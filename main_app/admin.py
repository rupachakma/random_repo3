from django.contrib import admin

from main_app.models import Category, CustomUser, JobPost, Skill

# Register your models here.
admin.site.register(Skill)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(JobPost)