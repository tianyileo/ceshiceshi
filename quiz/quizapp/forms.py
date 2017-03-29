from django import forms
from django.core.exceptions import ValidationError


def password_validator(comment):
    if len(comment) < 6:
        raise ValidationError(u"密码不少于6位")

class LoginForm(forms.Form):
    name = forms.CharField(required=True)
    # 用户邮箱
    email = forms.CharField(required=True)

    # 用户密码
    password = forms.CharField(
        required=True,
        error_messages = {
            "required": u'密码不能为空'
            },
        validators = [password_validator]
        )

class RegisterForm(forms.Form):
    # 用户名
    name = forms.CharField(required=True)

    # 用户邮箱
    email = forms.EmailField(required=True)

    # 用户密码
    password = forms.CharField(
        error_messages = {
            "required": u'密码不能为空'
            },
        validators = [password_validator]
        )


class ProfileForm(forms.Form):
    # 用户头像
    avatar = forms.ImageField()

    # 用户描述
    desc = forms.CharField(initial=u"这个用户很懒，还没有描述信息")


class QuestionForm(forms.Form):
    # 标题
    title = forms.CharField(required=True)

    # 问题描述
    desc = forms.CharField(required=True)

    # 主题描述
    topic = forms.CharField(required=True)

class AnswerForm(forms.Form):
    content = forms.CharField(required=True)

class VoteForm(forms.Form):
    vote = forms.CharField(required=True)
