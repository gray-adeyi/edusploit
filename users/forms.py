from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("identifier",)


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ("identifier",)
