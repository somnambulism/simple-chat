# -*- coding: utf-8 -*- 

from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('msg',)

    def clean(self):
        msg = self.cleaned_data.get('msg')
        if not msg:
            raise forms.ValidationError(u'Ooups, this should not happen, your message is empty')
        return self.cleaned_data

    def save(self, user, commit=True):
        obj = super(MessageForm, self).save(False)
        obj.user = user
        obj.username = user.username
        if commit:
            obj.save()
        return obj

    def get_errors(self):
        from django.utils.encoding import force_unicode
        output = {}
        for key, value in self.errors.items():
            output[key] = '/n'.join([force_unicode(i) for i in value])
        return output
