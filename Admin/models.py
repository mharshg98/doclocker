from django.db import models
from django.utils import timezone
from django_mysql.models import JSONField
# Create your models here.
class Student(models.Model):
    choices = ( ("CIVIENG_FT" , "CIVIENG_FT"), ("COMPENG_FT" , "COMPENG_FT"), ("ECIENG_FT", "ECIENG_FT"), ("ECTELEG_FT", "ECTELEG_FT"), ("ITENG_FT", "ITENG_FT"), ("MECHENG_FT", "MECHENG_FT"),  )
    id=models.AutoField(primary_key=True)
    section=models.CharField(null=True,max_length=1)
    branch=models.CharField(choices = choices,max_length=100)
    enrollment=models.CharField(unique=True,max_length=7)
    name=models.CharField(max_length=100)
    session=models.CharField(null=True,max_length=100)
    email=models.EmailField(unique=True,null=True)
    mobile=models.CharField(null=True,max_length=10)

    def __str__(self):
        return self.enrollment

class Enroll_Data(models.Model):
    sheet_id = models.AutoField(primary_key = True)
    date = models.DateTimeField(default = timezone.now)
    enroll_datasheet = models.FileField(upload_to = 'enroll_datasheets')

class Marksheet(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    marksheet_URL=models.JSONField(null=True)
    receipt_URL=models.JSONField(null=True)

class Subjects(models.Model):
    sem=models.IntegerField()
    sub_name=models.CharField(max_length=50)
    branch=models.CharField(max_length=5)
    theory_credit=models.IntegerField()
    practical_credit=models.IntegerField()
