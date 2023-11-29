from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # имя человека, отпраляющего пост
    email = forms.EmailField() # почта отправителя
    to = forms.EmailField() # почта получателя
    comments = forms.CharField(required=False, # является опциональным
                               widget=forms.Textarea) # комментарий вставляется в письмо