from django import forms
from MAC_profile import models



class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, label = "Username",widget = forms.TextInput(attrs={'required':'required'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'required':'required'}), label = "Password")
    passwordConfirm = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'required':'required'}), label = "Confirm Password")
    gender = forms.ChoiceField(choices=models.GENDERS,label="Gender")
    email = forms.EmailField(label="Email Address", widget = forms.TextInput(attrs={'required':'required','placeholder':'Enter a Email Valid Address'}))
    test = forms.CharField(max_length=6, label = "What University is this Club based out of?",widget = forms.TextInput(attrs={'required':'required'}))

class PassResetForm(forms.Form):
    username = forms.CharField(max_length=30, label = "Username",widget = forms.TextInput(attrs={'required':'required'}))
    reset_code = forms.CharField(max_length=200, label = "Reset Code",widget = forms.TextInput(attrs={'required':'required'}))

class NewPassForm(forms.Form):
    old_password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'required':'required'}), label = "Old Password")
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'required':'required'}), label = "New Password")
    passwordConfirm = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'required':'required'}), label = "Confirm New Password")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('display_name', 'tpp', 'ppp', 'location', 'gender', 'timezone', 'avatar_local', 'blurb', 'sig', 'website_url', 'website_text', 'steam_account', 'psn_account', 'xbox_account')
