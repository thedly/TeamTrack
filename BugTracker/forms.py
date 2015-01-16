from django import forms
from TaskManager.models import Projects, ExtendedUser, Tasks

class CreateBugForm(forms.Form):
    Title = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title'}))
    TaskId = forms.ModelChoiceField(label='', queryset=Tasks.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    Description = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'What Happened ?'}))
    UserId = forms.ModelChoiceField(label='', queryset=ExtendedUser.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))