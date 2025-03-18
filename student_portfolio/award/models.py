import os
import datetime

from django.db import models
import django
from django.contrib.auth.models import User


# Create your models here.
from django.dispatch import receiver
from private_storage.fields import PrivateFileField

from event.models import Skill
from student_portfolio.settings import PRIVATE_STORAGE_ROOT


def award_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return PRIVATE_STORAGE_ROOT + '//{0}_{1}_{2}'.format('award', instance.id, filename)

class Award(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    rank = models.IntegerField(default=0)

    received_date = models.DateField(default=datetime.date.today, blank=False)


    info = models.CharField(max_length=200, blank=True, default='')

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                   related_name='award_created_by_set', editable=True)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                    related_name='award_approved_by_set', editable=True, blank=True)

    used_for_calculation = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = PrivateFileField(upload_to=award_attachment_file_directory_path, max_file_size=2000000,
                                      null=True, blank=True, max_length=500)

    #Many to Many fields
    skills = models.ManyToManyField(Skill, related_name='award_skill_set', null=True)
    receivers = models.ManyToManyField(User, related_name='award_receiver_set', null=True)
    supervisors = models.ManyToManyField(User, related_name='award_supervisor_set', null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.title)

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=Award)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.attachment_file:
        _delete_file(instance.attachment_file.path)