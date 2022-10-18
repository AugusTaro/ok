from django.contrib import admin
from . models import user_expansions,category,video
# Register your models here.

admin.site.register(user_expansions)
admin.site.register(category)
admin.site.register(video)