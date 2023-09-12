from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, mail_managers





class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        mail_managers(
            subject="Новый пользователь!",
            message=f'Пользователь {user.username} зарегистрировался на сайте'
        )

        send_mail(
            subject="Вуелкам!",
            message=f'{user.username}, вам удалось каким то чудом зарегистрироваться, поздравляем!',
            from_email=None,
            recipient_list=[user.email],
        )

        common_users = Group.objects.get(name="Пользователи")
        user.groups.add(common_users)
        return user



