from django import forms

class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())
    thread_id = forms.IntegerField(widget=forms.HiddenInput())
    post_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

class ThreadForm(forms.Form):
    subject = forms.CharField(label = "Subject",widget = forms.TextInput(attrs={'required':'required'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'required':'required'}), label = "Contents")
    category_id = forms.IntegerField(widget=forms.HiddenInput())
