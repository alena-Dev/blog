from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # имя человека, отпраляющего пост
    email = forms.EmailField() # почта отправителя
    to = forms.EmailField() # почта получателя
    comments = forms.CharField(required=False, # является опциональным
                               widget=forms.Textarea) # комментарий вставляется в письмо
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # чтобы создать форму из модели
        fields = ['name', 'email', 'body'] # включить только эти поля