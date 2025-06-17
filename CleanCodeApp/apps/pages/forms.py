from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from uuid import uuid4

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            # Automatically create a Doctor profile with a unique doctor_id
            from .models import Doctor  # avoid circular import
            Doctor.objects.create(user=user, doctor_id=str(uuid4())[:8].upper())

        return user
