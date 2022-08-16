from django.contrib import admin
from .models import Meeting, Topic, Activity, Company, Outside, TopicFile, Signature, Category

admin.site.register(Meeting)
admin.site.register(Topic)
admin.site.register(Activity)
admin.site.register(Company)
admin.site.register(Outside)
admin.site.register(TopicFile)
admin.site.register(Signature)
admin.site.register(Category)
