from rest_framework import serializers
import json
from django.contrib.auth.models import User


from event.serializers import EventSerializer
from .access_policies import AwardApiAccessPolicy
from .models import Award
from event.models import Skill

from rest_access_policy import FieldAccessMixin, AccessPolicy
# from .access_policies import ProjectApiAccessPolicy

class AwardSkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Skill
        fields = ('id',)


class AwardReceiverSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('id',)


class AwardSupervisorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('id',)


class AwardSerializer(FieldAccessMixin, serializers.ModelSerializer):

    id = serializers.IntegerField(required=False, read_only=True)

    title = serializers.CharField(max_length=100, required=True)
    rank = serializers.IntegerField(required=False, read_only=False, min_value=0)
    received_date = serializers.DateField(required=False)

    info = serializers.CharField(max_length=200, allow_blank=True, required=False)

    created_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False, queryset=User.objects.all())

    approved = serializers.BooleanField(required=False)
    approved_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False, queryset=User.objects.all())
    used_for_calculation = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)
    attachment_file = serializers.FileField(required=False, allow_null=True)

    skills = AwardSkillSerializer(many=True, read_only=False, allow_null=True, required=False)
    receivers = AwardSkillSerializer(many=True, read_only=False, allow_null=True, required=False)
    supervisors = AwardSupervisorSerializer(many=True, read_only=False, allow_null=True, required=False)

    class Meta:
        model = Award
        fields = '__all__'

        access_policy = AwardApiAccessPolicy
    def create(self, validated_data):
        skills = validated_data.pop('skills', None)
        supervisors = validated_data.pop('supervisors', None)
        receivers = validated_data.pop('receivers', None)
        attachment_file = validated_data.pop('attachment_file', None)

        instance = Award.objects.create(**validated_data)

        if attachment_file is not None:
            instance.attachment_file = attachment_file

        if skills is not None:
            instance.skills.clear()
            for e in skills:
                instance.skills.add(Skill.objects.get(id=e['id']))

        if receivers is not None:
            instance.receivers.clear()
            for e in receivers:
                instance.receivers.add(User.objects.get(id=e['id']))

        if supervisors is not None:
            instance.supervisors.clear()
            for e in supervisors:
                instance.supervisors.add(User.objects.get(id=e['id']))

        instance.save()
        return instance

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.received_date = validated_data.get('received_date', instance.received_date)
        instance.info = validated_data.get('info', instance.info)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.used_for_calculation = validated_data.get('used_for_calculation', instance.used_for_calculation)
        instance.attachment_link = validated_data.get('attachment_link', instance.attachment_link)

        instance.attachment_file = validated_data.get('attachment_file', instance.attachment_file)

        # Update many-to-many relationships
        instance.skills.clear()
        if 'skills' in validated_data:
            for e in validated_data.get('skills'):
                instance.skills.add(Skill.objects.get(id=e['id']))

        instance.receivers.clear()
        if 'receivers' in validated_data:
            for e in validated_data.get('receivers'):
                instance.receivers.add(User.objects.get(id=e['id']))

        instance.supervisors.clear()
        if 'supervisors' in validated_data:
            for e in validated_data.get('supervisors'):
                instance.supervisors.add(User.objects.get(id=e['id']))

        instance.save()
        return instance

    @staticmethod
    def custom_clean_receivers(instance=None, data=None, context=None):
        # Check if the ids are present in the User table and Make them unique.
        # Assume that data is a stringnified object.
        user_ids = User.objects.all().values_list('id', flat=True)
        field_name = 'id'

        list_of_dicts = json.loads(data)

        if not (isinstance(list_of_dicts, list)) or len(
                list_of_dicts) == 0:  # If it is not a list, return an empty string ''. So that we could pop this field.
            return ''

        # Do We really need this???
        unique_ids = []
        out_list = []
        for e in list_of_dicts:

            id = e['id']
            if id not in user_ids:
                raise serializers.ValidationError(
                    "The user id is not present in the User table : " + str(e['id']))

            if id not in unique_ids:
                unique_ids.append(id)
                out_list.append(e)

        return out_list

    @staticmethod
    def custom_clean(instance=None, data=None, context=None ):

        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)

        #Clean data


        if 'skills' in data:
            data['skills'] = EventSerializer.custom_clean_skills(
                data=data['skills'])  # If it contains errors, the function will return a string, might be ''.
            if isinstance(data.get('skills', None), str):
                data.pop('skills', None)

        if 'receivers' in data:
            data['receivers'] = AwardSerializer.custom_clean_receivers(
                data=data['receivers'])  # If it contains errors, the function will return a string, might be ''.
            if isinstance(data.get('receivers', None), str):
                data.pop('receivers', None)

        if 'supervisors' in data:
            data['supervisors'] = AwardSerializer.custom_clean_receivers(
                data=data['supervisors'])  # If it contains errors, the function will return a string, might be ''.
            if isinstance(data.get('supervisors', None), str):
                data.pop('supervisors', None)

        if method == 'POST':
            data['created_by'] = request.user.id

            attachment_file = data.get('attachment_file', None)
            if isinstance(attachment_file, str):
                data.pop('attachment_file', None)

            if 'staff' in groups:
                if data.get('approved', None) == 'true':
                    data['approved_by'] = request.user.id
                else:
                    data['approved_by'] = None
            else:
                data.pop('approved', None)
                data.pop('approved_by', None)

        elif method == 'PUT':
            attachment_file = data.get('attachment_file', None)
            if isinstance(attachment_file, str):
                if attachment_file == '':  # We want '' to signal delete.
                    instance.attachment_file = None
                data.pop('attachment_file', None)


            if 'staff' in groups:
                if data.get('approved', None) == 'true':
                    if not instance.approved:
                        data['approved_by'] = request.user.id
                    else:
                        data.pop('approved_by', None)
                else:
                    data['approved_by'] = None
            else:
                data.pop('approved', None)
                data.pop('approved_by', None)

        return instance, data

    def validate_attachment_file(self, file):
        if file.size > 2000000:
            raise serializers.ValidationError("The file size must be less than 2 mb.")
        return file

    def validate_approved_by(self, approved_by):
        if approved_by == 'null' or approved_by == '':
            return None
        return approved_by