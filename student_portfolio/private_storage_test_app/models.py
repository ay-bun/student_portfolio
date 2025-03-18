from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from private_storage.fields import PrivateFileField
from private_storage.storage.files import PrivateFileSystemStorage

import os

from student_portfolio.settings import PRIVATE_STORAGE_ROOT


# my_storage = PrivateFileSystemStorage(
#     location= PRIVATE_STORAGE_ROOT + 'private_storage_test_app/{0}/{1}'.format(),
#     base_url='/private-media/'
# )

def private_test_model_private_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return PRIVATE_STORAGE_ROOT + '\{0}_{1}_{2}'.format('testprivate', instance.id, filename)

class PrivateModel(models.Model):

    id = models.BigAutoField(primary_key=True)
    private_file_1 = PrivateFileField(upload_to=private_test_model_private_file_directory_path, max_file_size=1024*1024*2,
                                      null=True, blank=True, max_length=500)
    private_file_2 = PrivateFileField(upload_to=private_test_model_private_file_directory_path, max_file_size=1024*1024*2,
                                      null=True, blank=True, max_length=500)

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='privatemodel_created_by_set', editable=False)

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=PrivateModel)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.private_file_1:
        _delete_file(instance.private_file_1.path)

    if instance.private_file_2:
        _delete_file(instance.private_file_2.path)
