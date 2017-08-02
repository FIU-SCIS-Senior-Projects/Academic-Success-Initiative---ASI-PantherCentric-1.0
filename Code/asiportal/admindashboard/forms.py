from django import forms
class NoteForm(forms.Form):		
    note = forms.CharField(label='note', max_length=140)
