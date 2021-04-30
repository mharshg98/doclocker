from django.db import models

# Create your models here.
class Student(models.Model):
    choices = ( ("CSA" , "CSA"), ("CSB" , "CSB"), ("ITA", "ITA"), ("ITB", "ITB"), ("ETCA", "ETCA"), ("CIVIL", "CIVIL"), ("MECH", "MECH") )
    id=models.AutoField(primary_key=True)
    branch=models.CharField(choices = choices,max_length=100)
    enrollment=models.CharField(unique=True,max_length=7)
    name=models.CharField(max_length=100)
    session=models.CharField(null=False,max_length=100)
    email=models.EmailField(unique=True,null=False)
    mobile=models.CharField(null=False,max_length=10)

    def __str__(self):
        return self.enrollment