# Generated by Django 3.2 on 2021-05-02 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_auto_20210430_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marksheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marksheet_URL', models.JSONField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.student')),
            ],
        ),
    ]