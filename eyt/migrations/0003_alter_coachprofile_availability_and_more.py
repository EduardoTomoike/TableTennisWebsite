# Generated by Django 5.1.1 on 2024-10-22 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyt', '0002_coachprofile_playerprofile_coachreview_videoreview_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachprofile',
            name='availability',
            field=models.CharField(blank=True, default='Unknown', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='coachprofile',
            name='experience_years',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coachprofile',
            name='specialization',
            field=models.CharField(default='General', max_length=100),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='specialization',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
