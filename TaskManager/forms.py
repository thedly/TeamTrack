from django import forms
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,send_mass_mail
from TaskManager.models import ExtendedUser
class UpdatesForTodayForm(forms.Form):
    TaskNotes = forms.CharField(widget=forms.Textarea(attrs={'class':'varcharData','placeholder':'SCR1234: Gathered requirements'}))

class SearchForm(forms.Form):
    Search = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Search for tasks,projects & profiles','id':'MainSearchBar','lang':'en','x-webkit-speech':''}))
     
class LoginForm(forms.Form):
    Username = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Username'}))
    Password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'varcharData','placeholder':'Password'}))

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ('username','first_name','last_name','is_superuser','groups','email','password','birthdate','rating')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

    
class MailForm(forms.Form):
    To = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'To'}))
    UsersTo = forms.ModelChoiceField(label='',queryset = User.objects.all(),widget=forms.SelectMultiple(attrs={'class':'varcharData'}))
    Cc = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Cc'}))
    UsersCc = forms.ModelChoiceField(label='',queryset = User.objects.all(),widget=forms.SelectMultiple(attrs={'class':'varcharData'}))
    Subject = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Subject'}))
    Message = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'varcharData','placeholder':'Message'}))
    
    def send_email(self):
        message = EmailMessage(subject=self.Subject,
                       body=self.Message,
                       from_email=self.sender,
                       to=self.to_addresses,
                       bcc=self.cc_addresses,
                       headers={'Cc': ','.join(self.cc_addresses)})
        message.send()
#         datatuple = (
#             ('Subject', 'Message.', 'from@example.com', ['john@example.com']),
#             ('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
#         )
#         send_mass_mail(datatuple)
    
class AddClientForm(forms.Form):
    Name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Name'}))
    Email = forms.EmailField(label='',widget=forms.TextInput(attrs={'class':'varcharData','placeholder':'Email'}))
    ContactNumber = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'integerData','placeholder':'Contact NUmber'}))
    AlternateContactNumber = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'integerData','placeholder':'Alternate number'}))
    