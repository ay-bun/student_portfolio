from datetime import datetime

from rest_access_policy import FieldAccessMixin, AccessPolicy
from django.db.models import Q

from event.models import EventAttendance


class EventApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>", "<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"

        },

    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        groups = request.user.groups.values_list('name', flat=True)
        method = request.method


        if method == "GET":
            pass


        # Cleaning data
        if method == "POST":
            fields.pop('id', None)

            if 'staff'in groups:
                pass
            elif 'student' in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        elif method == "PUT":
            fields.pop('created_by')

            if 'staff' in groups:
                pass
            elif 'student' in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        return fields

    @classmethod
    def scope_query_object(cls, request):

        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            lower_bound_start_datetime = request.GET.get('lower_bound_start_datetime', None)
            upper_bound_start_datetime = request.GET.get('upper_bound_start_datetime', None)
            used_for_calculation = request.GET.get('used_for_calculation', None)

            query_object = Q()
            if used_for_calculation is not None:
                query_object &= Q(used_for_calculation=(used_for_calculation == 'true'))

            if lower_bound_start_datetime is not None:
                query_object &= Q(start_datetime__gte=datetime.strptime(lower_bound_start_datetime, '%Y-%m-%dT%H:%M:%S.%fZ'))

            if upper_bound_start_datetime is not None:
                query_object &= Q(start_datetime__lte=datetime.strptime(upper_bound_start_datetime, '%Y-%m-%dT%H:%M:%S.%fZ'))

            if 'staff' in groups:
                return query_object

            elif 'student' in groups:
                return query_object & (Q(approved=True) | Q(created_by=request.user.id))

        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(approved=False) & Q(created_by=request.user.id)

        elif request.method == "DELETE":

            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(approved=False) & Q(created_by=request.user.id)

class EventAttendanceApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>", "<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff"],
            "effect": "allow"
        },
        {
            "action": ["<method:get>"],
            "principal": ["group:student"],
            "effect": "allow",
        },

    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "POST":
            fields.pop('id', None)

        elif request.method == "PUT":
            fields.pop('event_id', None)

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)
        if request.method == "GET":
            if 'staff' in groups:
                return Q()
            elif 'student' in groups:
                return Q(user_id_fk=request.user.id)
        elif request.method == "POST":
            if 'staff' in groups:
                return Q()
        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()
        elif request.method == "DELETE":
            if 'staff' in groups:
                return Q()


class CurriculumApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff"],
            "effect": "allow"

        },

        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },

    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        if request.method == "POST":
            fields.pop('id', None)
        elif request.method == "PUT":
            pass

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()
            elif 'student' in groups:
                return Q()

        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()

        elif request.method == "DELETE":
            if 'staff' in groups:
                return Q()

class SkillGroupApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff"],
            "effect": "allow"

        },
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
        {   #We do not need this part.
            "action": ["<method:put>"],
            "principal": ["group:student"],
            "effect": "deny"
        },
    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        if request.method == "POST":
            fields.pop("id", None)
            # fields = {'name': fields.get('name', None)}

        elif request.method == "PUT":
            pass

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()
            elif 'student' in groups:
                return Q()

        elif request.method == "PUT":
            return Q()

        elif request.method == "DELETE":
            return Q()


class SyncStudentAttendanceByStudentIdAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:put>"],
            "principal": ["group:staff"],
            "effect": "allow"
        },
    ]

class SkillTableApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
        {
            "action": ["<method:put>", "<method:post>"],
            "principal": ["group:staff"],
            "effect": "deny"
        },
        {
            "action": ["<method:delete>"],
            "principal": ["*"],
            "effect": "deny"
        },
    ]
    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        if request.method == "POST":
            fields.pop("id", None)

        elif request.method == "PUT":
            pass

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()
            elif 'student' in groups:
                return Q()
            else: #unauthenticated user.
                return Q()
        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()

        elif request.method == "DELETE":
            #CurrentlyDisabled
            pass



class EventAttendedListApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"

        },
    ]

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            query_object = Q()

            event_attendance_used_for_calculation = request.GET.get('event_attendance_used_for_calculation', None)
            if event_attendance_used_for_calculation is not None:
                if event_attendance_used_for_calculation == 'true':
                    event_attendance_used_for_calculation = True
                else:
                    event_attendance_used_for_calculation = False

                attendances = EventAttendance.objects.filter(synced=True, user_id_fk=request.user.id,
                                                             used_for_calculation=event_attendance_used_for_calculation)

            else:
                attendances = EventAttendance.objects.filter(synced=True, user_id_fk=request.user.id)

            event_ids = attendances.values_list('event_id_fk', flat=True)

            event_used_for_calculation = request.GET.get('event_used_for_calculation', None)
            if event_attendance_used_for_calculation is not None:
                event_used_for_calculation = bool(event_used_for_calculation)
                query_object &= Q(used_for_calculation=event_used_for_calculation)

            if 'staff' in groups:
                query_object &= Q(approved=True) & Q(id__in=event_ids)
            elif 'student' in groups:
                query_object &= Q(approved=True) & Q(id__in=event_ids)

            return query_object

class EventAttendanceBulkAddApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:post>"],
            "principal": ["group:staff"],
            "effect": "allow"

        },
    ]

class EventCurriculumSummaryApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff"],
            "effect": "allow"

        },
    ]