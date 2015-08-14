from __future__ import unicode_literals
from __future__ import print_function

from django.db import models


class NoticeManager(models.Manager):
    def notices_for(self, user, archived=False, unseen=None, sent=False):
        if sent:
            lookup_kwargs = {"sender": user}
        else:
            lookup_kwargs = {"recipient": user}
        qs = self.filter(**lookup_kwargs)
        if not archived:
            qs = qs.filter(archived=archived)
        if unseen is not None:
            qs = qs.filter(unseen=unseen)
        return qs

    def unseen_count_for(self, recipient, **kwargs):
        return self.notices_for(recipient, unseen=True, **kwargs).count()
