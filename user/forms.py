from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
import re


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Istifadeci adi", required=True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=100, label="Shifre", required=True,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            return users.first().username.lower()
        return username.lower()

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Shifre ve ya Ad yanlishdir")

class RegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=6, max_length=100, label="Istifadeci adi")
    password = forms.CharField(max_length=100, label="Shifre", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label="Shifre tesdiq", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password", "password2"]

    # Bootstrap desteklesin deye edirik bunun evezine CRISPY de istifade etmek olar
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username.lower()

    def clean_password2(self):
        pswd_1 = self.cleaned_data.get("password")
        pswd_2 = self.cleaned_data.get("password2")
        if pswd_1 and pswd_2 and pswd_1 != pswd_2:
            raise forms.ValidationError("Shifreler eyni olmalidir")
        return pswd_2

class UpdateForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=UserProfile.SEX_FIELD, required=True)
    profile_photo = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False, max_length=200)

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields["bio"].widget.attrs['rows'] = 4

    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_photo", "sex", "bio"]

