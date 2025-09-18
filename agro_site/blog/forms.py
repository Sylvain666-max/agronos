from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label='Recherche', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher...'}))
