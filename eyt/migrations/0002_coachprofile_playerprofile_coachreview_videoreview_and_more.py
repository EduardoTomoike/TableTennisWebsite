# Generated by Django 5.1.1 on 2024-10-14 00:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoachProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
                ('experience_years', models.IntegerField()),
                ('certifications', models.CharField(blank=True, max_length=255, null=True)),
                ('availability', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.FloatField(default=0.0)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('specialization', models.CharField(max_length=100)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoachReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review_text', models.TextField()),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eyt.coachprofile')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eyt.playerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='VideoReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('rating', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eyt.coachprofile')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eyt.video')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualCoachingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('completed', 'Completed')], max_length=50)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eyt.coachprofile')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eyt.playerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending')], max_length=50)),
                ('session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eyt.virtualcoachingsession')),
            ],
        ),
    ]