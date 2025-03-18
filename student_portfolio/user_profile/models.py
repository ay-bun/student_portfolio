from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from event.models import Curriculum


class FacultyRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, default='')

    def __str__(self):
        return "{} {}".format(self.id, self.name)

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)

    university_id  = models.CharField(max_length=11, blank=True, default='', unique=True)
    user_id_fk = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    firstname   = models.CharField(max_length=50, blank=True, default='')
    middlename  = models.CharField(max_length=50, blank=True, default='')
    lastname    = models.CharField(max_length=50, blank=True, default='')
    
    email = models.EmailField(max_length=254, blank=True, default='')

    faculty_role = models.ForeignKey(FacultyRole, null=True, on_delete=models.SET_NULL)

    enroll = models.ForeignKey(Curriculum, null=True, on_delete=models.SET_NULL,
                               related_name='userprofile_enroll_set', blank=True)

    def __str__(self):
        return "{} {} {} {} {}".format(self.id, self.university_id, self.firstname,
                                       self.lastname, self.faculty_role.name)


