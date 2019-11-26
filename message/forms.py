from django import forms
from .models import MessageNew

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget = forms.Textarea(attrs={"class": "form-control"})
        self.fields["content"].widget.attrs["rows"] = 3

    class Meta:
        model = MessageNew
        fields = ["content"]