# Generated by Django 4.0.3 on 2022-05-24 08:28

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('short_code', models.CharField(blank=True, max_length=5, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('parent_holding', models.BooleanField()),
                ('status_active', models.BooleanField()),
                ('company_type', models.CharField(choices=[('OW', 'Mining Owner'), ('TR', 'Coal Trading'), ('CR', 'Mining Contractor'), ('OT', 'Others')], max_length=2)),
                ('location_ho', models.CharField(blank=True, max_length=100, null=True)),
                ('location_site', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('meeting_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('notulen', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('meeting2company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company2meeting', to='pica.company', verbose_name='Company')),
                ('meeting2user', models.ManyToManyField(related_name='user2meeting', to=settings.AUTH_USER_MODEL, verbose_name='Peserta Internal')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('topic_name', models.CharField(blank=True, max_length=100, null=True)),
                ('problem_info', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('action', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('new_due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('O', 'Open'), ('C', 'Close'), ('A', 'Archive')], default='O', max_length=1)),
                ('issue_date', models.DateField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('topic2company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company2topic', to='pica.company', verbose_name='Problem owner')),
                ('topic2department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department2topic', to='users.department', verbose_name='Department')),
                ('topic2meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting2topic', to='pica.meeting', verbose_name='Meeting')),
                ('topic2user', models.ManyToManyField(related_name='user2topic', to=settings.AUTH_USER_MODEL, verbose_name='PIC')),
            ],
        ),
        migrations.CreateModel(
            name='TopicFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('doc_file', models.FileField(blank=True, null=True, upload_to='topic/file/%Y/%m/%d')),
                ('topicfile2topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic2topicfile', to='pica.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('position', models.CharField(blank=True, max_length=50, null=True)),
                ('company_code', models.CharField(blank=True, max_length=5, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('signature2profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile2signature', to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Outside',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('photo', models.ImageField(default='profile/user-default.png', upload_to='outside/')),
                ('company_from', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('outside2meeting', models.ManyToManyField(blank=True, related_name='meeting2outside', to='pica.meeting', verbose_name='Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('doc_file', models.FileField(blank=True, null=True, upload_to='activity/file/%Y/%m/%d')),
                ('activityfile2activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity2activityfile', to='pica.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('activity_date', models.DateField(auto_now=True, unique=True)),
                ('action_short_description', models.CharField(blank=True, max_length=100, null=True)),
                ('action_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('activity2topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic2activity', to='pica.topic', verbose_name='Related Topic')),
                ('activity2user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2activity', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
        ),
    ]
