# from django.db import models
# from django.contrib.auth.models import User
#
# # Create your models here.
# class Student(models.Model):
#     id = models.BigAutoField(primary_key=True)
#
#     student_id  = models.CharField(max_length=11, blank=True, default='')
#     user_id_fk = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#
#     firstname   = models.CharField(max_length=50, blank=True, default='')
#     middlename  = models.CharField(max_length=50, blank=True, default='')
#     lastname    = models.CharField(max_length=50, blank=True, default='')
#
#     def __str__(self):
#         return "{} {} {} {}".format(self.id, self.student_id, self.firstname, self.lastname)