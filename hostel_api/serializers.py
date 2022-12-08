from rest_framework import serializers
from pydantic import BaseModel
from django.db.utils import IntegrityError

from .models import (
    User,
    Staff,
    Student,
    Resident,
    Room,
    Building,
)


class BuildingShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ['id', 'number', 'address']


class StaffSerializer(serializers.ModelSerializer):
    buildings = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ['id', 'surname', 'name', 'patronymic', 'buildings']

    def get_buildings(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'buildings' in include_fields:
            return BuildingShortSerializer(obj.buildings.all(), many=True).data

        return [building.number for building in obj.buildings.all()]


class BuildingSerializer(serializers.ModelSerializer):
    staff = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ['id', 'number', 'address', 'staff']

    def get_staff(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'staff' in include_fields:
            return StaffSerializer(obj.staff.all(), many=True).data

        return [staff.__str__() for staff in obj.staff.all()]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'surname',
            'name',
            'patronymic',
            'grade',
            'group',
            'study_direction',
            'student_card',
            'birth_date',
            'enter_date'
        ]

    def create(self, validated_data):
        try:
            user = User.objects.create(username=validated_data['student_card'])
            user.set_password(validated_data['birth_date'].strftime('%d.%m.%Y'))
            user.save()
        except IntegrityError:
            raise serializers.ValidationError({'error': 'Такой студент уже зарегистрирован'})
        validated_data['user_id'] = user.id
        return super().create(validated_data)


class RoomShortSerializer(serializers.ModelSerializer):
    building = serializers.IntegerField(source='building.number')

    class Meta:
        model = Room
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        fields = ['id', 'student', 'photo', 'room', 'contract', 'registration', 'address']

    def get_student(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'student' in include_fields:
            return StudentSerializer(obj.student).data

        return obj.student.__str__()

    def get_room(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'room' in include_fields:
            return RoomShortSerializer(obj.room).data

        return obj.room.number


class ResidentCreateSerializer(ResidentSerializer):
    student = serializers.IntegerField(write_only=True)
    room = serializers.CharField()
    contract = serializers.FileField(required=False,)
    registration = serializers.FileField(required=False)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Resident
        fields = ['id', 'student', 'photo', 'room', 'contract', 'registration']

    def create(self, validated_data):
        return super().create(validated_data)

    def validate_student(self, value):
        try:
            student = Student.objects.get(student_card=value)
            try:
                student.resident
                raise serializers.ValidationError('Студент уже заселен')
            except Student.resident.RelatedObjectDoesNotExist:
                return student
        except Student.DoesNotExist:
            raise serializers.ValidationError('Студент не найден')

    def validate_room(self, value):
        building_num, room_num = value.split('-')
        try:
            room = Room.objects.get(number=room_num, building__number=building_num)
            if room.resident_set.count() == room.max_residents:
                raise serializers.ValidationError('Комната полностью заселена')
            return room
        except Room.DoesNotExist:
            raise serializers.ValidationError('Комната не найдена')


class RelocateRoomResidentSchema(BaseModel):
    room_id: int
    resident_id: int
