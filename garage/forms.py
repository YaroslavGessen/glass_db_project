from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from garage.models import Vehicles, Glasses, CustomUser, Vectors


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicles
        fields = ['v_number', 'v_manufacture', 'v_model', 'v_date_of_prod']
        widgets = {'v_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'v_manufacture': forms.TextInput(attrs={'class': 'form-control'}),
                   'v_model': forms.TextInput(attrs={'class': 'form-control'}),
                   'v_date_of_prod': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                   }


class GlassForm(forms.ModelForm):
    class Meta:
        model = Glasses
        fields = ['g_source', 'g_damage_type', 'g_damage_side', 'g_nak', 'g_mgk', 'g_alk',
                  'g_sik', 'g_sk', 'g_cik', 'g_kka', 'g_kkb', 'g_caka', 'g_cakb', 'g_tik',
                  'g_crk', 'g_mnk', 'g_fek', 'g_coka', 'g_cuka', 'g_cukb', 'g_znka', 'g_znkb',
                  'g_srk', 'g_model']
        widgets = {'g_source': forms.TextInput(attrs={'class': 'form-control'}),
                   'g_damage_type': forms.TextInput(attrs={'class': 'form-control'}),
                   'g_damage_side': forms.TextInput(attrs={'class': 'form-control'}),
                   'g_nak': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_mgk': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_alk': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_sik': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_sk': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_cik': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_kka': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_kkb': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_caka': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_cakb': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_tik': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_crk': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_mnk': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_fek': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_coka': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_cuka': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_cukb': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_znka': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_znkb': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_srk': forms.NumberInput(attrs={'class': 'form-control'}),
                   'g_model': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'True'}),
                   }


class VectorsForm(forms.ModelForm):
    model = Vectors
    fields = ['v_source', 'json_data']
    widgets = {'v_source': forms.TextInput(attrs={'class': 'form-control'}),
               'json_data': forms.Textarea(attrs={'class': 'form-control'})}


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('image', 'username', 'first_name', 'email', 'is_viewer', 'is_editor')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('image', 'username', 'email')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
