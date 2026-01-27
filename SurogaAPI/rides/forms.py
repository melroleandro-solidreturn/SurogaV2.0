from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.utils.translation import gettext_lazy

from core.models import User
from rides.models import paymentlog

