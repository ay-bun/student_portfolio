from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):

    userId = serializers.IntegerField(required=False)
    studentId = serializers.CharField(min_length=11, max_length=11, required=False, allow_blank=True)

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    class Meta:
        model = Student
        fields = ('userId', 'studentId', 'firstname', 'middlename', 'lastname')