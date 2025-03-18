from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Event, EventAttendance, Skill, Skillgroup, Curriculum, AssignSkillToSkillgroup
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User

from rest_access_policy import FieldAccessMixin, AccessPolicy
from .access_policies import EventApiAccessPolicy, EventAttendanceApiAccessPolicy, CurriculumApiAccessPolicy, \
    SkillGroupApiAccessPolicy, EventAttendanceBulkAddApiAccessPolicy, SkillTableApiAccessPolicy

from datetime import datetime
import json
import csv


class SkillSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(max_length=50, required=True)
    info = serializers.CharField(max_length=200, required=False, allow_blank=True)
    # goal_point = serializers.IntegerField(min_value=0, max_value=10,  required=False)

    class Meta:
        model = Skill
        fields = ('id', 'title', 'info')
        access_policy = SkillTableApiAccessPolicy

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        # request = context['request']
        # method = request.method
        # groups = request.user.groups.values_list('name', flat=True)

        return instance, data

class EventSkillSerializer( serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Skill
        fields = ('id',)


class EventStaffSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('id',)


class EventSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    start_datetime = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M")
    end_datetime = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M")

    info = serializers.CharField(max_length=200, allow_blank=True, required=False)

    created_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False,
                                                    queryset=User.objects.all())
    approved = serializers.BooleanField(required=False)
    approved_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False,
                                                     queryset=User.objects.all())

    used_for_calculation = serializers.BooleanField(required=False)
    arranged_inside = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)

    attachment_file = serializers.FileField(required=False, allow_null=True)

    skills = EventSkillSerializer(many=True, read_only=False, allow_null=True, required=False)
    staffs = EventStaffSerializer(many=True, read_only=False, allow_null=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_datetime', 'end_datetime', 'info', 'created_by',
                  'approved', 'approved_by', 'used_for_calculation', 'arranged_inside', 'attachment_link',
                  'attachment_file', 'skills', 'staffs')

        access_policy = EventApiAccessPolicy
    def create(self, validated_data):
        skills = validated_data.pop('skills', None)
        staffs = validated_data.pop('staffs', None)
        attachment_file = validated_data.pop('attachment_file', None)

        instance = Event.objects.create(**validated_data)

        if attachment_file is not None:
            instance.attachment_file = attachment_file


        if skills is not None:
            instance.skills.clear()
            for e in skills:
                instance.skills.add(Skill.objects.get(id=e['id']))

        if staffs is not None:
            instance.staffs.clear()
            for e in staffs:
                instance.staffs.add(User.objects.get(id=e['id']))

        instance.save()
        return instance

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.start_datetime = validated_data.get('start_datetime', instance.start_datetime)
        instance.end_datetime = validated_data.get('end_datetime', instance.end_datetime)
        instance.info = validated_data.get('info', instance.info)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.used_for_calculation = validated_data.get('used_for_calculation', instance.used_for_calculation)
        instance.arranged_inside = validated_data.get('arranged_inside', instance.arranged_inside)
        instance.attachment_link = validated_data.get('attachment_link', instance.attachment_link)

        instance.attachment_file = validated_data.get('attachment_file', instance.attachment_file)

        # Update many-to-many relationships
        instance.skills.clear()
        if 'skills' in validated_data:
            for e in validated_data.get('skills'):
                instance.skills.add(Skill.objects.get(id=e['id']))

        instance.staffs.clear()
        if 'staffs' in validated_data:
            for e in validated_data.get('staffs'):
                instance.staffs.add(User.objects.get(id=e['id']))

        instance.save()
        return instance

    def validate(self, data):

        start_datetime, end_datetime = (data.get('start_datetime', None), data.get('end_datetime', None))
        if start_datetime is not None and end_datetime is not None:
            # print("{} {} {}".format("start_datetime", type(start_datetime), start_datetime))
            # print("{} {} {}".format("end_datetime", type(end_datetime), end_datetime))
            if start_datetime > end_datetime:
                raise ValidationError("End datetime must be after start datetime.")
        elif (start_datetime is not None or end_datetime is not None):
            raise ValidationError("start_datetime and end_datetime must be present at the same time.")

        return data

    def validate_attachment_file(self, file):
        if file.size > 2000000:
            raise serializers.ValidationError("The file size must be less than 2 mb.")
        return file


    @staticmethod
    def custom_clean_skills(instance=None, data=None, context=None):

        # Assume that data is a stringnified object.
        skill_ids = Skill.objects.all().values_list('id', flat=True)

        # print(data)
        list_of_dicts = json.loads(data)
        # print(type(list_of_dicts))
        # print(list_of_dicts)

        if not (isinstance(list_of_dicts, list)) or len(
                list_of_dicts) == 0:  # If it is not a list, return an empty string ''. So that we could pop this field.
            return ''

        # Do We really need this???
        unique_ids = []
        out_list = []
        for e in list_of_dicts:

            id = e['id']
            if id not in skill_ids:
                raise serializers.ValidationError(
                    "The skill id is not present in the Skill table : " + str(e['id']))

            if id not in unique_ids:
                unique_ids.append(id)
                out_list.append(e)

        return out_list

    @staticmethod
    def custom_clean_staffs(instance=None, data=None, context=None):
        user_ids = User.objects.all().values_list('id', flat=True)
        # Need to check for correctness and redundancies.
        list_of_dicts = json.loads(data)

        if not (isinstance(list_of_dicts, list)) or len(
                list_of_dicts) == 0:  # If it is not a list, return an empty string ''. So that we could pop this field.
            return ''

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
    def custom_clean(instance=None, data=None, context=None):
        # print(data)
        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)

        if 'skills' in data:
            data['skills'] = EventSerializer.custom_clean_skills(
                data=data['skills'])  # If it contains errors, the function will return a string, might be ''.
            if isinstance(data.get('skills', None), str):
                data.pop('skills', None)

        if 'staffs' in data:
            data['staffs'] = EventSerializer.custom_clean_staffs(data=data['staffs'])
            if isinstance(data.get('staffs', None), str):
                data.pop('staffs', None)


        if method == 'POST':
            data['created_by'] = request.user.id

            if 'staff' in groups:
                if data.get('approved', None) == 'true':
                    data['approved_by'] = request.user.id
                else:
                    data['approved_by'] = None
            else:
                data.pop('approved', None)
                data.pop('approved_by', None)

            attachment_file = data.get('attachment_file', None)
            if isinstance(attachment_file, str):
                data.pop('attachment_file', None)

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
                data.pop("approved", None)
                data.pop("approved_by", None)

        return instance, data

    def validate_approved_by(self, approved_by):
        if approved_by == 'null' or approved_by == '':
            return None
        return approved_by

class EventAttendanceSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    event_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=True,
                                                     queryset=Event.objects.all())

    university_id = serializers.CharField(min_length=11, max_length=11, required=True)

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    user_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False,
                                                    queryset=User.objects.all())

    synced = serializers.BooleanField(required=False)
    used_for_calculation = serializers.BooleanField(required=False)

    class Meta:
        model = EventAttendance
        fields = ('id', 'event_id_fk', 'university_id', 'firstname', 'middlename', 'lastname',
                  'user_id_fk', 'synced', 'used_for_calculation')

        access_policy = EventAttendanceApiAccessPolicy

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        request = context['request']
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "POST":
            pass
        if request.method == "PUT":
            data['synced'] = 'false' #We won't let this in if the university is not present.

            if 'user_id_fk' in data:
                student_id_fk = data['user_id_fk']
                if student_id_fk == '' or student_id_fk == 'null':
                    data.pop('user_id_fk', None)

        return instance, data

class EventAttendanceBulkAddSerializer(FieldAccessMixin, serializers.Serializer):

    event_id = serializers.IntegerField(required=True)
    csv_file = serializers.FileField(required=True, allow_empty_file=False)
    class Meta:
        # Model = EventAttendance
        fields = ('event_id', 'csv_file')
        access_policy = EventAttendanceBulkAddApiAccessPolicy

    def validate_event_id(self, event_id):
        instance = Event.objects.filter(id=event_id)

        if not instance.exists():
            raise ValidationError("The event_id = {} does not exist.".format(event_id))

        return event_id

    def validate_csv_file(self, file):
        if file.size > 2000000:
            raise ValidationError("The file size must be less than 2 mb.")
        return file



class CurriculumSkillGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Skillgroup
        fields = ('id',)


class CurriculumSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    th_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    en_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    start_date = serializers.DateField(required=False, format="%Y-%m-%d")
    end_date = serializers.DateField(required=False, format="%Y-%m-%d")
    info = serializers.CharField(max_length=200, allow_blank=True, required=False)

    attachment_file = serializers.FileField(required=False, allow_null=True)

    skillgroups = CurriculumSkillGroupSerializer(many=True, read_only=False, allow_null=True, required=False)

    class Meta:
        model = Curriculum
        fields = ('id', 'th_name', 'en_name', 'start_date', 'end_date', 'info', 'attachment_file', 'skillgroups')
        access_policy = CurriculumApiAccessPolicy
    def create(self, validated_data):

        skillgroups = validated_data.pop('skillgroups', None)
        attachment_file = validated_data.pop('attachment_file', None)

        instance = Curriculum.objects.create(**validated_data)

        if attachment_file is not None:
            instance.attachment_file = attachment_file

        instance.skillgroups.clear()
        if skillgroups is not None:
            for e in skillgroups:
                instance.skillgroups.add(Skillgroup.objects.get(id=e['id']))

        instance.save()
        return instance

    def update(self, instance, validated_data):

        instance.th_name = validated_data.get('th_name', instance.th_name)
        instance.en_name = validated_data.get('en_name', instance.en_name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.info = validated_data.get('info', instance.info)
        instance.attachment_file = validated_data.get('attachment_file', instance.attachment_file)

        instance.skillgroups.clear()
        if 'skillgroups' in validated_data:
            for e in validated_data.get('skillgroups'):
                instance.skillgroups.add(Skillgroup.objects.get(id=e['id']))

        instance.save()
        return instance

    @staticmethod
    def custom_clean_skillgroups(instance=None, data=None, context=None):

        skill_group_ids = Skillgroup.objects.all().values_list('id', flat=True)

        # print(data)
        list_of_dicts = json.loads(data)
        # print("list_of_dicts : {}".format(list_of_dicts))

        if not (isinstance(list_of_dicts, list)) or len(list_of_dicts) == 0:  # Pop from the caller.
            return None

        unique_ids = []
        out_list = []
        for e in list_of_dicts:

            id = e['id']
            if id not in skill_group_ids:
                raise serializers.ValidationError(
                    "The id is not present in the table : " + str(e['id']))

            if id not in unique_ids:
                unique_ids.append(id)
                out_list.append(e)

        return out_list

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        request = context['request']

        if 'skillgroups' in data:
            skillgroup = CurriculumSerializer.custom_clean_skillgroups(data=data.get('skillgroups', None))
            if skillgroup is None:
                data.pop('skillgroups', None)
            else:
                data['skillgroups'] = skillgroup

        # Handling Methods.
        if request.method == "POST":
            attachment_file = data.get('attachment_file', None)
            if isinstance(attachment_file, str):
                data.pop('attachment_file', None)

        elif request.method == 'PUT':
            attachment_file = data.get('attachment_file', None)
            if isinstance(attachment_file, str):
                if attachment_file == '':  # We want '' to signal delete.
                    instance.attachment_file = None
                data.pop('attachment_file', None)

        return (instance, data)

    def validate_attachment_file(self, file):
        if file.size > 2000000:
            raise serializers.ValidationError("The file size must be less than 2 mb.")
        return file

    def validate(self, data):
        start_date, end_date = (data.get('start_date', None), data.get('end_date', None))
        if start_date is not None and end_date is not None:
            # print("{} {} {}".format("start_datetime", type(start_datetime), start_datetime))
            # print("{} {} {}".format("end_datetime", type(end_datetime), end_datetime))
            if start_date > end_date:
                raise ValidationError("End date must be after start date.")

        elif start_date is not None or end_date is not None:
            raise ValidationError("start_date and end_date must be present at the same time.")

        return data

class CurriculumStudentBulkAddSerializer(serializers.Serializer):
    curriculum_id = serializers.IntegerField(required=True)
    csv_file = serializers.FileField(required=True, allow_empty_file=False)

    class Meta:
        # Model = EventAttendance
        fields = ('event_id', 'csv_file')

    def validate_curriculum_id(self, event_id):
        instance = Curriculum.objects.filter(id=event_id)

        if not instance.exists():
            raise ValidationError("The curriculum_id = {} does not exist.".format(event_id))

        return event_id

    def validate_csv_file(self, file):
        if file.size > 2000000:
            raise serializers.ValidationError("The file size must be less than 2 mb.")
        return file

class SkillAssignedToSkillGroup(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Skill
        fields = ('id',)


class AssignSkillToSkillgroupSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=True)
    # skillgroup_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False,
    #                                                       queryset=Skillgroup.objects.all())
    skill_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False,
                                                     queryset=Skill.objects.all())

    goal_point = serializers.FloatField(min_value=0, max_value=10, required=False)

    class Meta:
        model = AssignSkillToSkillgroup
        fields = ('skill_id_fk', 'goal_point')


class SkillGroupSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    info = serializers.CharField(max_length=200, allow_blank=True, required=False)

    # skills = SkillAssignedToSkillGroup(many=True, read_only=False, allow_null=True, required=False)
    skills = AssignSkillToSkillgroupSerializer(many=True, source='assignskilltoskillgroup_skillgroup_set',
                                               read_only=False, allow_null=True, required=False)

    class Meta:
        model = Skillgroup
        fields = ('id', 'name', 'info', 'skills')
        access_policy = SkillGroupApiAccessPolicy


    def create(self, validated_data):

        skills = validated_data.pop('assignskilltoskillgroup_skillgroup_set', None)

        instance = Skillgroup.objects.create(**validated_data)
        instance.skills.clear()

        if skills is not None:
            for e in skills:
                instance.skills.add(e['skill_id_fk'], through_defaults={'goal_point': e['goal_point']})

        instance.save()
        return instance

    def update(self, instance, validated_data):
        print(validated_data)
        instance.name = validated_data.get('name', instance.name)
        instance.info = validated_data.get('info', instance.info)

        instance.skills.clear()

        # Now we work with the related name : assignskilltoskillgroup_skillgroup_set
        # Note : validated_data contains THE OBJECTS, not primary keys.
        if 'assignskilltoskillgroup_skillgroup_set' in validated_data:
            for e in validated_data.get('assignskilltoskillgroup_skillgroup_set'):
                # The comment below shows an equivalent way of creating a relationship.
                AssignSkillToSkillgroup.objects.create(skillgroup_id_fk=instance,
                                                       skill_id_fk=e['skill_id_fk'],
                                                       goal_point=e['goal_point'])
                # instance.skills.add(e['skill_id_fk'],
                #                     through_defaults={'goal_point': e['goal_point']}
                #                     )

        instance.save()
        return instance

    @staticmethod
    def custom_clean_skills(instance=None, data=None, context=None):
        # Assume that data is a stringnified object.
        skill_ids = Skill.objects.all().values_list('id', flat=True)

        # print(data)
        list_of_dicts = json.loads(data, strict=False)
        # print(list_of_dicts)

        if (not isinstance(list_of_dicts, list)) or len(
                list_of_dicts) == 0:  # If it is not a list, return an empty string ''. So that we could pop this field.
            return ''
        print(list_of_dicts)
        # Do We really need this???
        unique_ids = []
        out_list = []
        for e in list_of_dicts:

            id = int(e['skill_id_fk'])
            if id not in skill_ids:
                raise serializers.ValidationError(
                    "The skill id is not present in the Skill table : " + id)

            if id not in unique_ids:
                unique_ids.append(id)
                out_list.append(e)

        # print('outlist {}'.format(out_list))
        # print(type(out_list))
        return out_list

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        request = context['request']

        if 'skills' in data:
            data['skills'] = SkillGroupSerializer.custom_clean_skills(data=data['skills'])
            if isinstance(data.get('skills', None), str):
                data.pop('skills', None)

        if request.method == "POST":
            pass

        elif request.method == "PUT":
            pass

        # print('in custom clean')
        # print(instance, data)
        return instance, data


