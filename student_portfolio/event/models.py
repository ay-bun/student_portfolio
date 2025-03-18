import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from private_storage.fields import PrivateFileField

from student_portfolio.settings import PRIVATE_STORAGE_ROOT


def event_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return PRIVATE_STORAGE_ROOT + '//{0}_{1}_{2}'.format('event', instance.id, filename)

class Skill(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=200, blank=True, default='')
    # goal_point = models.BigIntegerField(default=0)
    # info = models.CharField(max_length=200, default='')
    # detail = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Event(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(null=True, blank=False)
    end_datetime = models.DateTimeField(null=True, blank=False)

    info = models.CharField(max_length=200, blank=True, default='')

    # skills = models.JSONField(default=dict)

    #user_id
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='event_created_by_set', editable=False)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='event_approved_by_set')

    used_for_calculation = models.BooleanField(default=False)
    arranged_inside = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = PrivateFileField(upload_to=event_attachment_file_directory_path, max_file_size=2000000,
                                      null=True, blank=True, max_length=500)

    skills = models.ManyToManyField(Skill, related_name='event_skill_set', null=True)
    staffs = models.ManyToManyField(User, related_name='event_staff_set', null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.title)

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=Event)
def delete_file_event(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.attachment_file:
        _delete_file(instance.attachment_file.path)

class EventAttendance(models.Model):
    id = models.BigAutoField(primary_key=True)

    event_id_fk = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)
    university_id = models.CharField(max_length=11)

    firstname = models.CharField(max_length=50, blank=True, default='')
    middlename = models.CharField(max_length=50, blank=True, default='')
    lastname = models.CharField(max_length=50, blank=True, default='')

    user_id_fk = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    synced = models.BooleanField(default=False)
    used_for_calculation = models.BooleanField(default=False)




class Skillgroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    info = models.CharField(max_length=200, default='')

    skills = models.ManyToManyField(Skill, through='AssignSkillToSkillgroup', related_name='skillgroup_skill_set', null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.name)

class AssignSkillToSkillgroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    skillgroup_id_fk = models.ForeignKey(Skillgroup, on_delete=models.CASCADE, related_name='assignskilltoskillgroup_skillgroup_set')
    skill_id_fk = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='assignskilltoskillgroup_skill_set')

    goal_point = models.FloatField(default=0)

    def __str__(self):
        return "{} {}".format(self.id, self.goal_point)



def curriculum_attachment_file_directory_path(instance, filename):
    return PRIVATE_STORAGE_ROOT + '\{0}_{1}_{2}'.format('curriculum', instance.id, filename)

class Curriculum(models.Model):
    id = models.BigAutoField(primary_key=True)
    th_name = models.CharField(max_length=50, blank=True, default='')
    en_name = models.CharField(max_length=50, blank=True, default='')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    info = models.CharField(max_length=200, default='')
    attachment_file = PrivateFileField(upload_to=curriculum_attachment_file_directory_path,
                                       max_file_size=2000000,
                                       null=True, blank=True, max_length=500)

    skillgroups = models.ManyToManyField(Skillgroup, related_name='curriculum_skillgroup_set', null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.th_name)

@receiver(models.signals.post_delete, sender=Curriculum)
def delete_file_curriculum(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.attachment_file:
        _delete_file(instance.attachment_file.path)