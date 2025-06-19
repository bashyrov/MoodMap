from django import forms
from .models import CustomUser
from .models import Message, DiaryEntry, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz swoją wiadomość...',
            'style': 'height: 100px;',
        }),
        label=""
    )


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'date']

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz tytuł...'}),
        label="Tytuł",
        max_length=15
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz swoją notatkę do dziennika...',
            'style': 'height: 100px;'}),
        label="Treść"
    )

    date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2024, 2026), attrs={
            'class': 'form-control',
            'placeholder': 'Wybierz datę...',
        }),
        label="Data",
    )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'name@example.com',
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Password'
        }),
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com'
        }),
        label='Email',
        max_length=255,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

