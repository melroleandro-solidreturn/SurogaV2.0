import urllib.parse
import json
import logging
import time
import gevent

from django.utils import timezone
from django.conf import settings
from ws4py.websocket import WebSocket
from ws4py.server.geventserver import WSGIServer
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from ws4py.client.geventclient import WebSocketClient
from gevent import Greenlet
from gevent.lock import RLock
from gevent.pool import Pool
from api.janus_calls import createTask, editTask, destroyTask, activateTask, blockTask, countTask


import pprint
import random
import string
import asyncio

log = logging.getLogger(__name__)

from celery import shared_task
from .models import tasks_queue

class WSClient(WebSocketClient):

    APP_FACTORY = None
    DEFAULT_ENCODER = json.JSONEncoder()
    DEFAULT_DECODER = json.JSONDecoder()
    DEFAULT_MSG_HANDLE_THREAD_POOL_SIZE = 8

    def __init__(self, url, recv_msg_cbk=None, close_cbk=None, protocols=None, msg_encoder=None, msg_decoder=None):
        # patch socket.sendall to protect it with lock,
        # in order to prevent sending data from multiple greenlets concurrently
        WebSocketClient.__init__(self, url, protocols=protocols)
        self._msg_encoder = msg_encoder or self.DEFAULT_ENCODER
        self._msg_decoder = msg_decoder or self.DEFAULT_DECODER
        self.lock = RLock()
        self._sendall = self.sock.sendall
        self._recv_msg_cbk = recv_msg_cbk
        self._close_cbk = close_cbk
        

        self.connect()

    def __str__(self):
        return 'websocket client connection with {0}'.format(self.peer_address)

    def received_message(self, message):
        if message.is_text:
            if self._recv_msg_cbk:
                try:
                    self._recv_msg_cbk(self._msg_decoder.decode(str(message)))
                except Exception:
                    log.exception('Failed to handle received msg on {0}'.format(self))
                    raise

    def send_message(self, message, timeout=30):
        """
        send message
        :param message: object which can be encoded by msg_encoder (by default json encoder)
        :param timeout: send timeout in second, if timeout, gevent.Timeout exception will be raised
        :return:
        """
        self.send(self._msg_encoder.encode(message), binary=False)
        
    def closed(self, code, reason=None):
        if self._close_cbk:
            self._close_cbk()


def gen_random_key(length, chars=string.ascii_letters+string.digits):
    return ''.join([random.choice(chars) for n in range(length)])


class Janus(object):
    def __init__(self, base_url, transaction=None):
        self.s = WSClient(base_url, self._on_recv_msg, None, protocols=('janus-protocol',))
        self.base_url = base_url
        self.session_id = None
        self.transaction = transaction
        self.admin_key = settings.JANUS_SECRET
        self.task = None
        self.tasks = []
        self.errorCODE = None
        self.error = False
        self.plugin_handle_id = None
        self.payload = None
        self.Room = None
        self.Created = None
        self.task_item = None
        self.partecipants = None
        self.countPartecipants = 0

        if self.transaction is None:
            self.transaction = gen_random_key(16)

    def _on_recv_msg(self, msg):
        if 'janus' in msg.keys():
            if msg['janus']=='success':
                if self.task == 'session':
                    self.session_id =  msg['data']['id']
                if self.task == 'attach':
                    self.plugin_handle_id  =  msg['data']['id']
                if self.task == 'call':
                    self.Room  =  msg['plugindata']['data']['room']
                    self.Created  =  msg['plugindata']['data']['videoroom']
                if self.task == 'count':
                    self.participants  =  msg['plugindata']['data']['participants']
                    self.countPartecipants  =  len(self.participants)
                self.run()
            if msg['janus']=='error':
                self.errorCODE =  msg['error']['code']
                self.error = True
            if msg['janus']=='timeOut':
                self.errorCODE = 'timeOut'
                self.error = True

        return msg


    def request(self,  data):

        self.s.send_message(data)


    def acquire_session(self):
        self.task = 'session'
        self.request( {
            'janus': 'create',
            'transaction': self.transaction,
            'apisecret': self.admin_key,
        })


    def acquire_plugin(self, name):
        self.task = 'attach'
        return self.janus_call('attach', {
            'plugin': name,
        })
    

    def janus_call(self, method, payload):
        data = {
            'janus': method,
            'transaction': self.transaction,
            'apisecret': self.admin_key,
            'session_id': self.session_id,
        }
        data.update(payload)
        self.request( data)

    def plugin_call(self, payload):
        log.error('payload {0}'.format(payload))
        self.task = 'call'
        self.request({
            'janus': 'message',
            'apisecret': self.admin_key,
            'session_id': self.session_id,
            'handle_id': self.plugin_handle_id,
            'body': payload,
            'transaction': self.transaction,
        })

    
    def run(self):   
        if self.tasks:
            task = self.tasks.pop(0)
            if not self.error:
                if task == 'acquire_session':
                    gevent.joinall([gevent.spawn(self.acquire_session())])
                if task == 'acquire_plugin':
                    self.acquire_plugin('janus.plugin.videoroom')
                if task == 'plugin_call':
                    self.plugin_call(self.payload)
                if task == 'keepalive':
                    self.janus_call('keepalive',{})
        else:
            if not self.error:
                log.error('Update DB')
                if self.task_item.command=='create':
                    self.task_item.key.Room = self.Room
                    self.task_item.key.Status = 1
                    self.task_item.key.save()
                if self.task_item.command=='destroy': 
                    self.task_item.key.Deleted = True
                    self.task_item.key.save()
                if self.task_item.command=='count': 
                    self.task_item.key.NumParticipants = self.countPartecipants
                    self.task_item.key.maxNumParticipants = max(self.task_item.key.maxNumParticipants,self.countPartecipants)
                    self.task_item.key.save()
                self.task_item.delete() 
            else:
                if self.task_item.command=='create':
                    self.task_item.key.Status = 2
                    self.task_item.key.save()
                
                if self.task_item.CountTries > 5:
                    self.task_item.delete()
                else:
                    self.task_item.CountTries += 1
                    self.task_item.save()
                log.error('Update DB error')
            self.s.close()
        
        


@shared_task
def janus_feed():
    jsonDec = json.decoder.JSONDecoder()
    
    listTask = tasks_queue.objects.all().order_by('Priority','RegistrationDate')
    if listTask:

        for task in listTask:
            code = jsonDec.decode(task.Code)
            log.error(code)  

            j = Janus(settings.JANUSAPI)
            
            j.tasks =[ 'acquire_session', 'acquire_plugin','plugin_call']
            j.payload = code
            j.task_item = task
            j.run()



    


