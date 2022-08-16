from django.contrib import admin
from .models import Profile, Department


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'bod', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department)
