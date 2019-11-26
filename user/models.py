from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
from uuid import uuid4
from message.models import MessageNew

# Create your models here.

# Shekili save etmeden evvel adini deyishir



def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_name = "{}.{}".format(str(uuid4()), extension)
    return os.path.join("profile", new_name)


class UserProfile(models.Model):
    SEX_FIELD = ((None, "Cinsiyyet"), ("male", "Kisi"), ("female", "Qadin"))
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, verbose_name="Haqqimda", blank=True)
    profile_photo = models.ImageField(blank=True, default="default/default-profile.png", upload_to=upload_to,
                                      verbose_name="Profil shekili")
    sex = models.CharField(choices=SEX_FIELD, blank=True, max_length=6, verbose_name="Cinsiyyet")

    def get_name_for_screen(self):
        user = self.user
        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def get_userprofile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return '/media/default/default-profile.png'

    def get_all_username(self):
        # Butun Istifadecileri getirir
        username_list = User.objects.values_list("username", float=True)
        return username_list

    def __str__(self):
        return "{} -Profile".format(self.get_name_for_screen())


def create_profile(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)
