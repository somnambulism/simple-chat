# -*- coding: utf-8 -*- 

from django.db import models
from django.conf import settings


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    username = models.CharField(max_length=30)
    msg = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return str(self.created_at)
