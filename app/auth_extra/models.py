# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from authtools.models import AbstractEmailUser
from rest_framework.authtoken.models import Token

@python_2_unicode_compatible
class UserSettings(models.Model):

    ###################################################################
    # for efficient lookup of user settings we store them directly in
    # the user table (via abstract model).
    # eventually this has to be changed in the future.
    ###################################################################

    class Meta(AbstractEmailUser.Meta):
        app_label = 'auth_extra'
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')
        abstract = True


    def __str__(self):
        return '<UserSettings> {}'.format(self.pk)




@python_2_unicode_compatible
class User(AbstractEmailUser, UserSettings):

    """
    user model holds only information needed for authentication.
    all further information is stored in the one-to-one related 'profile'
    model.
    """

    # used by social auth
    username = models.CharField(
        _('Username'),
        max_length=128, null=True, blank=True,
        help_text=_('This is used by 3rd party auth only')
    )

    # email verification
    email_verified = models.BooleanField(default=False)



    class Meta(AbstractEmailUser.Meta):
        app_label = 'auth_extra'
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')


    def __str__(self):
        if self.username:
            return '{}'.format(self.username)
        return '{}'.format(self.email)

    def get_full_name(self):
        if self.profile and self.profile.full_name:
            return self.profile.full_name
        if self.username:
            return self.username
        return self.email

    def get_short_name(self):
        return self.username


    def save(self, *args, **kw):
        if self.pk is not None:
            _orig = User.objects.get(pk=self.pk)
            if _orig.email != self.email:
                self.email_verified = False
        super(User, self).save(*args, **kw)



@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
