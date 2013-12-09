# -*- coding: utf-8 -*- 

import json

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import DateFormat

from .models import Message
from .forms import MessageForm

from gevent.event import Event


class Chat(object):
    def __init__(self):
        self.new_msg_event = Event()

    def write_message(self, request):
        if not request.user.is_authenticated() or request.method != 'POST':
            return HttpResponse(status=404)
        form = MessageForm(request.POST)
        output = dict(success=False)
        if form.is_valid():
            form.save(request.user)
            output['success'] = True
        else:
            output['errors'] = form.get_errors()
        self.new_msg_event.set()
        self.new_msg_event.clear()
        return HttpResponse(json.dumps(output))

    def get_messages(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(status=404)
        pk = int(request.GET.get('pk', 1))
        messages = [{'created_at': DateFormat(el.created_at).format('H:i:s'),
                    'username': el.username, 'pk': el.pk,
                    'msg': el.msg} for el in Message.objects.filter(pk__gt=int(pk))
                                            .order_by('-created_at')[:100]]
        if not messages:
            self.new_msg_event.wait()
        return HttpResponse(json.dumps(messages[::-1]))


@login_required
def view_chat(request):
    return render(request, 'chat.jade', {})

chat = Chat()
write_message, get_messages = (chat.write_message, chat.get_messages)
