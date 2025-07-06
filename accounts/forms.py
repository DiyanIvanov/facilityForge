from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class  CustomRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'email')