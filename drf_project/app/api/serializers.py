from rest_framework import  serializers
from ..models import (
    Address,
    Teacher,
    Student,
    TeacherProfile
)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        # fields = ('street', 'country', 'region', )
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()

    class Meta:
        model = Teacher
        fields = '__all__'


"""
While Using nested serializer overrding create for creation and update for
updating is must
"""
class TeacherProfileSerializer(serializers.ModelSerializer):

    profile = TeacherSerializer()

    class Meta:
        model = TeacherProfile
        fields = ('profile', 'description', 'email', )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        teacher_address = profile_data.pop('address')
        teacher_obj, created = Teacher.objects.get_or_create(**profile_data)
        teacher_obj.address.add(*teacher_address)
        profile_obj, created = TeacherProfile.objects.get_or_create(profile=teacher_obj, **validated_data)
        return profile_obj

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        profile_address = profile.pop('address')
        for key, value in profile.items():   #  can be done using update feature of orm
            setattr(instance.profile, key, value)
        instance.profile.save()
        instance.profile.address.clear()
        instance.profile.address.add(*profile_address)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class StudentOnlySerializer(serializers.ModelSerializer):

  class Meta:
      model = Student
      fields = '__all__'


"""
While Using nested serializer overrding create for creation and update for
updating is must
"""
class StudentSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=True)

    class Meta:
        model = Student
        fields = ('picture', 'documents', 'name', 'phone', 'is_obident', 'teacher', 'address')

    def create(self, validated_data):
        teacher_data = validated_data.pop('teacher')
        teacher_address = teacher_data.pop('address')
        teacher_obj, created = Teacher.objects.get_or_create(**teacher_data)
        teacher_obj.address.add(*teacher_address)
        student_address = validated_data.pop('address')
        if student_address:
            address_obj, created = Address.objects.get_or_create(**student_address[0])
        student, created = Student.objects.get_or_create(teacher=teacher_obj, **validated_data)
        student.address.add(address_obj)
        return student

    def update(self, instance, validated_data):
        teacher_data = validated_data.pop('teacher')
        teacher_address = teacher_data.pop('address')
        teacher_obj, created = Teacher.objects.get_or_create(**teacher_data)
        teacher_obj.address.add(*teacher_address)
        student_address = validated_data.pop('address')[0]
        address_obj, created = Address.objects.get_or_create(**student_address)
        student, created = Student.objects.get_or_create(teacher=teacher_obj, **validated_data)
        student.address.add(address_obj)
        return instance


