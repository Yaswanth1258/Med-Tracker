from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'dosage_amount', 'dosage_unit', 'frequency_amount', 'frequency_unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'dosage_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency_unit': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="I am a...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Assign group
            group = self.cleaned_data['group']
            user.groups.add(group)
        return user
