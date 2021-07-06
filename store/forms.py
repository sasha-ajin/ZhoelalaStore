from django.forms import ModelForm, Form,CharField,PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginUserForm(Form):
    username = CharField(label='username', max_length=100)
    password = CharField(widget=PasswordInput())



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
