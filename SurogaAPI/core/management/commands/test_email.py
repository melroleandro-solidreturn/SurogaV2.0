# email_app/management/commands/test_email.py
from django.core.management.base import BaseCommand
from core.extras import EmailThread  # Ajuste o caminho!

class Command(BaseCommand):
    help = 'Testa envio de e-mail via SMTP Contabo'

    def handle(self, *args, **options):
        # Construa o dicionário no formato esperado
        email_data = {
            "message": {
                "subject": "Teste de Configuração SMTP",
                "body": {
                    "contentType": "HTML",  # Pode ser "Text" ou "HTML"
                    "content": """
                    <h2>✅ Teste Bem-Sucedido!</h2>
                    <p>Esta mensagem confirma que sua configuração SMTP com a Contabo está funcionando.</p>
                    <p><strong>Detalhes:</strong></p>
                    <ul>
                      <li>Servidor: smtp.contabo.com</li>
                      <li>Porta: 587</li>
                      <li>Usuário: api@greenconnections.eu</li>
                    </ul>
                    """
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": "melro.leandro@protonmail.com"
                        }
                    }
                ]
            }
        }

        # Dispara o e-mail em thread separada
        EmailThread(email_data).start()

        self.stdout.write(self.style.SUCCESS('E-mail de teste enviado! Verifique sua caixa de entrada.'))