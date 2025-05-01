from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from blog.models import Profile

class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url', 'facebook', 'instagram', 'twitter')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'website_url': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget = forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget = forms.TextInput(attrs={'class': 'form-control'}))

    class Meta: 
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Hacer que estos campos se vean solo como texto (sin editar)
    last_login = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=False
    )
    date_joined = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=False
    )

    # Hacer que estos campos no sean editables
    is_superuser = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False, disabled=True)
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False, disabled=True)
    is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False)
    # Verificar si el usuario es superusuario para habilitar los campos is_superuser e is_staff
    is_superuser = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False)
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False)
    is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False)

    # Estos campos estarán deshabilitados para usuarios no superusuario
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if not self.instance.is_superuser:
            # Si no es superusuario, deshabilitar los campos is_superuser e is_staff
            self.fields['is_superuser'].disabled = True
            self.fields['is_staff'].disabled = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100, widget = forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=100, widget = forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password2 = forms.CharField(max_length=100, widget = forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    class Meta: 
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
