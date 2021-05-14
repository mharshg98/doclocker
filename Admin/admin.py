from django.contrib import admin
from .models import Student,Marksheet,Enroll_Data,Subjects
# Register your models here.

admin.site.register(Student)
admin.site.register(Marksheet)
admin.site.register(Enroll_Data)
admin.site.register(Subjects)
