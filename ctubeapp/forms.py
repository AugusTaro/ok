from django import forms
from django.contrib.auth.forms import AuthenticationForm #追加

# ----------------InputForm クラスの下に追加します-------------
# ログインフォーム
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class SerchForm(forms.Form):
    Name      = forms.CharField()
    #category  = forms.IntegerField()