from django.db import models


"""
Teacher Can Have many students and address are many to many field on both table(student and teacher)
Teacher has one to one field to its related profile
"""


class Address(models.Model):
    street = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'address is {self.country} {self.region} {self.street}'

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Address'


class AbstractDetailModel(models.Model):
    name = models.CharField(max_length=255)
    phone = models.PositiveIntegerField(default=0, unique=True)

    class Meta:
        abstract = True


class Teacher(AbstractDetailModel):
    Degree = models.CharField(max_length=255, blank=True)
    salary = models.PositiveIntegerField(default=0)
    address = models.ManyToManyField(Address, related_name='teachers')

    def __str__(self):
        return self.name


def get_deleted_teacher():
    return Teacher.objects.get(name='Deleted User')[0]


class Student(AbstractDetailModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET(get_deleted_teacher))
    picture = models.ImageField(upload_to='student_image', blank=True)
    documents = models.FileField(upload_to='student_docs', blank=True)
    address = models.ManyToManyField(Address, related_name='students')
    is_obident = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    profile = models.OneToOneField(Teacher, related_name='profile', on_delete=models.CASCADE)
    description = models.TextField()
    email = models.EmailField(blank=True, unique=True)

    def __str__(self):
        return f'Profile of {self.profile.name}'



