from django.contrib import admin

from .models import Address, Teacher, Student, TeacherProfile

admin.site.register([TeacherProfile, Address, Teacher, Student, ])