from zoneinfo import available_timezones
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Staff, UserProfile, ROLE_CHOICES, phone_validator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime
from django.utils import timezone

date_validator = RegexValidator(
    regex=r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$',
    message="Дата должна быть в формате DD/MM/YYYY"
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Phone number',
        max_length=20,
        required=True,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375 (29) XXX-XX-XX'}),
        error_messages={
            'required': 'Поле "Phone number" обязательно для заполнения',
            'invalid': 'Номер телефона должен быть в формате: +375 (29) XXX-XX-XX'
        }
    )
    birth_date = forms.CharField(
        label='Birthday date',
        required=True,
        validators=[date_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}),
        error_messages={
            'required': 'Поле "Birthday date" обязательно для заполнения',
            'invalid': 'Дата должна быть в формате DD/MM/YYYY'
        }
    )
    
    timezone = forms.ChoiceField(
        label="Timezone",
        choices=[(tz, tz) for tz in sorted(available_timezones())],
        initial='UTC',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': f'Поле {field.label} обязательно для заполнения',
                'invalid': f'Поле {field.label} заполнено некорректно'
            }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise ValidationError("Этот номер телефона уже зарегистрирован.")
        return phone

    def clean_birth_date(self):
        birth_date_str = self.cleaned_data.get('birth_date')
        try:
            birth_date = datetime.strptime(birth_date_str, '%d/%m/%Y').date()
            today = datetime.now().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise ValidationError("Вам должно быть не менее 18 лет.")
            return birth_date
        except ValueError:
            raise ValidationError("Неверный формат даты. Используйте формат DD/MM/YYYY (например, 01/01/2000)")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                birth_date=self.cleaned_data['birth_date'],
                timezone=self.cleaned_data['timezone'],
                role='client'
            )
        return user

class StaffForm(forms.ModelForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Номер телефона',
        max_length=20,
        required=True,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375 (29) XXX-XX-XX'}),
        error_messages={
            'required': 'Поле "Номер телефона" обязательно для заполнения',
            'invalid': 'Номер телефона должен быть в формате: +375 (29) XXX-XX-XX'
        }
    )
    birth_date = forms.CharField(
        label='Дата рождения',
        required=True,
        validators=[date_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}),
        error_messages={
            'required': 'Поле "Дата рождения" обязательно для заполнения',
            'invalid': 'Дата должна быть в формате DD/MM/YYYY'
        }
    )
    
    timezone = forms.ChoiceField(
        label="Часовой пояс",
        choices=[(tz, tz) for tz in sorted(available_timezones())],
        initial='UTC',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Staff
        fields = ['photo', 'position', 'experience']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise ValidationError("Этот номер телефона уже зарегистрирован.")
        return phone

    def clean_birth_date(self):
        birth_date_str = self.cleaned_data.get('birth_date')
        try:
            birth_date = datetime.strptime(birth_date_str, '%d/%m/%Y').date()
            today = datetime.now().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise ValidationError("Вам должно быть не менее 18 лет.")
            return birth_date
        except ValueError:
            raise ValidationError("Неверный формат даты. Используйте формат DD/MM/YYYY (например, 01/01/2000)")

    def save(self, commit=True):
        staff = super().save(commit=False)
        if commit:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            user_profile = UserProfile.objects.create(
                user=user,
                role='agent',
                phone_number=self.cleaned_data['phone_number'],
                birth_date=self.cleaned_data['birth_date'],
                timezone=self.cleaned_data['timezone'],
            )
            staff.user_profile = user_profile
            staff.save()
        return staff 