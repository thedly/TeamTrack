from django import forms
from django.contrib.auth.models import User

class UpdatesForTodayForm(forms.Form):
    TaskNotes = forms.CharField(widget=forms.Textarea(attrs={'class':'varcharData','placeholder':'SCR1234: Gathered requirements'}))

class SearchForm(forms.Form):
    Search = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Search for tasks,projects & profiles','id':'MainSearchBar'}))
     
class LoginForm(forms.Form):
    Username = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Username'}))
    Password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'varcharData','placeholder':'Password'}))
    
class MailForm(forms.Form):
    To = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'To'}))
    UsersTo = forms.ModelChoiceField(label='',queryset = User.objects.all(),widget=forms.SelectMultiple(attrs={'class':'varcharData'}))
    Cc = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Cc'}))
    UsersCc = forms.ModelChoiceField(label='',queryset = User.objects.all(),widget=forms.SelectMultiple(attrs={'class':'varcharData'}))
    Subject = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Subject'}))
    Message = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'varcharData','placeholder':'Message'}))
    
class AddClientForm(forms.Form):
    Name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Name'}))
    Email = forms.EmailField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Email'}))
    ContactNumber = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'integerData','placeholder':'Contact NUmber'}))
    AlternateContactNumber = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'integerData','placeholder':'Alternate number'}))
    