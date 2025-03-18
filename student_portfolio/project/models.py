import datetime
import os

from django.db import models
from django.dispatch import receiver

from event.models import Skill
from django.contrib.auth.models import User
import django

from private_storage.fields import PrivateFileField
from student_portfolio.settings import PRIVATE_STORAGE_ROOT

def project_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return PRIVATE_STORAGE_ROOT + '//{0}_{1}_{2}'.format('project', instance.id, filename)


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    start_date = models.DateField(default=datetime.date.today, blank=False)
    end_date = models.DateField(default=datetime.date.today, blank=False)

    info = models.CharField(max_length=200, blank=True, default='')

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                   related_name='project_created_by_set', editable=False)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                    related_name='project_approved_by_set', editable=False)

    used_for_calculation = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = PrivateFileField(upload_to=project_attachment_file_directory_path, max_file_size=2000000, null=True, blank=True, max_length=500)

    skills = models.ManyToManyField(Skill, related_name='project_skill_set', null=True)
    staffs = models.ManyToManyField(User, related_name='project_staff_set', null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.title)

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=Project)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.attachment_file:
        _delete_file(instance.attachment_file.path)
