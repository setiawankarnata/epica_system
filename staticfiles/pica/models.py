from django.db import models
from django.contrib.auth.models import User
from users.models import Department, Profile
import uuid


class Company(models.Model):
    CHOICE_TYPE_COMPANY = [
        ('OW', 'Mining Owner'),
        ('TR', 'Coal Trading'),
        ('CR', 'Mining Contractor'),
        ('OT', 'Others')
    ]
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    short_code = models.CharField(max_length=5, null=True, blank=True)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    parent_holding = models.BooleanField()
    status_active = models.BooleanField()
    company_type = models.CharField(max_length=2, choices=CHOICE_TYPE_COMPANY)
    location_ho = models.CharField(max_length=100, null=True, blank=True)
    location_site = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Signature(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    level = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    signature2profile = models.ForeignKey(Profile, related_name="profile2signature", on_delete=models.CASCADE,
                                          null=True, blank=True)
    company_code = models.CharField(max_length=5, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.position} - {self.company_code}"


class Meeting(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    meeting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    notulen = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    meeting2company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company2meeting",
                                        verbose_name="Company")
    meeting2user = models.ManyToManyField(User, related_name='user2meeting', verbose_name="Peserta Internal")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meeting {self.meeting2company.short_code}, {self.meeting_date}"


class Outside(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    photo = models.ImageField(upload_to="outside/", default='profile/user-default.png')
    company_from = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    outside2meeting = models.ManyToManyField(Meeting, verbose_name="Meeting",
                                             related_name="meeting2outside", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    @property
    def photo_url(self):
        try:
            url = self.photo.url
        except NameError:
            url = ''
        return url


class Topic(models.Model):
    CHOICE_STATUS = [
        ('O', 'Open'),
        ('C', 'Close'),
        ('A', 'Archive')
    ]
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    topic_name = models.CharField(max_length=100, null=True, blank=True)
    # problem_info = RichTextUploadingField(null=True, blank=True)
    # action = RichTextUploadingField(null=True, blank=True)
    problem_info = models.TextField(blank=True, null=True)
    action = models.TextField(null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    new_due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=CHOICE_STATUS, default="O")
    issue_date = models.DateField(blank=True, null=True)
    topic2department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Department",
                                         related_name="department2topic")
    topic2meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name="Meeting",
                                      related_name="meeting2topic")
    topic2company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name="company2topic", verbose_name="Problem owner")
    topic2user = models.ManyToManyField(User, verbose_name="PIC", related_name="user2topic")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic_name


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    activity_date = models.DateField(auto_now=True, unique=True)
    action_short_description = models.CharField(max_length=100, null=True, blank=True)
    action_description = models.TextField(null=True, blank=True)
    activity2topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Related Topic",
                                       related_name="topic2activity")
    activity2user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Updated by",
                                      related_name="user2activity")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity2user.username} - {self.activity_date}"


class TopicFile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    topicfile2topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name="topic2topicfile")
    doc_file = models.FileField(upload_to='topic/file/%Y/%m/%d', null=True, blank=True)


class ActivityFile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    activityfile2activity = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name="activity2activityfile")
    doc_file = models.FileField(upload_to='activity/file/%Y/%m/%d', null=True, blank=True)
