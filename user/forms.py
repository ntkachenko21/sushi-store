from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.models import CustomUser
import uuid


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

    def save(self, commit=True):
        user = super().save(commit=False)

        base_username = self.cleaned_data['email'].split('@')[0]
        username = base_username

        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}_{uuid.uuid4().hex[:6]}"

        user.username = username

        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })