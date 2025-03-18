from rest_framework import serializers
from .models import Staff
from django.contrib.auth.models import User

class StaffSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    staff_id = serializers.CharField(min_length=11, max_length=11, required=False, allow_blank=True)
    user_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, queryset=User.objects.all())

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    class Meta:
        model = Staff
        fields = ('id', 'staff_id', 'user_id_fk', 'firstname', 'middlename', 'lastname')
