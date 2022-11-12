from rest_framework import serializers
import factory

from .models import (
    Staff,
    Student,
    Resident,
    Room,
    Building,
    Grade
)


class BuildingShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ['number', 'address']


class StaffSerializer(serializers.ModelSerializer):
    buildings = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ['surname', 'name', 'patronymic', 'buildings']

    def get_buildings(self, obj):
        include_fields = self.context.get('include')
        if 'buildings' in include_fields:
            return BuildingShortSerializer(obj.buildings.all(), many=True).data

        return [building.id for building in obj.buildings.all()]


class BuildingSerializer(serializers.ModelSerializer):
    staff = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ['number', 'address', 'staff']

    def get_staff(self, obj):
        include_fields = self.context.get('include')
        if 'staff' in include_fields:
            return StaffSerializer(obj.staff.all(), many=True).data

        return [staff.id for staff in obj.staff.all()]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['auth_token', 'pass_hash']


class RoomShortSerializer(serializers.ModelSerializer):
    building = serializers.IntegerField(source='building.number')

    class Meta:
        model = Room
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(source='grade.name')
    student = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        fields = ['student', 'grade', 'photo', 'birth_date',
                  'enter_date', 'room', 'contract', 'registration', 'address']

    def get_student(self, obj):
        include_fields = self.context.get('include')
        if 'student' in include_fields:
            return StudentSerializer(obj.student).data

        return obj.student.id

    def get_room(self, obj):
        include_fields = self.context.get('include')
        if 'room' in include_fields:
            return RoomShortSerializer(obj.room).data

        return obj.room.number


class ResidentCreateSerializer(ResidentSerializer):
    grade = serializers.CharField(write_only=True)
    student = serializers.IntegerField(write_only=True)
    room = serializers.CharField(write_only=True)
    contract = serializers.FileField(required=False, write_only=True)
    registration = serializers.FileField(required=False, write_only=True)
    photo = serializers.ImageField(write_only=True)
    birth_date = serializers.DateField(write_only=True)
    enter_date = serializers.DateField(write_only=True)

    class Meta:
        model = Resident
        fields = ['student', 'grade', 'photo', 'birth_date',
                  'enter_date', 'room', 'contract', 'registration']

    def create(self, validated_data):
        return super().create(validated_data)

    def validate_grade(self, value):
        try:
            grade = Grade.objects.get(name=value)
            return grade
        except Grade.DoesNotExist:
            raise serializers.ValidationError('Ступень обучения не найдена')

    def validate_student(self, value):
        try:
            student = Student.objects.get(student_card=value)
            if student.resident is None:
                return student
            raise serializers.ValidationError('Студент уже заселен')
        except Student.DoesNotExist:
            raise serializers.ValidationError('Студент не найден')

    def validate_room(self, value):
        building_num, room_num = value.split('-')
        try:
            room = Room.objects.get(number=room_num, building__number=building_num)
            return room
        except Room.DoesNotExist:
            raise serializers.ValidationError('Студент не найден')

    def validate_contract(self, value):
        if value is None:
            return factory.django.FileField()
        return value

    def validate_registration(self, value):
        if value is None:
            return factory.django.FileField()
        return value
