from django import forms
from .models import Customer
from django.contrib.auth.forms import  AuthenticationForm

class SignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
        'password': forms.PasswordInput(),
    }


class LoginForm(AuthenticationForm):
    class Meta:
        model = Customer

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

class TransferForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    recipient_account_number = forms.CharField(max_length=10)