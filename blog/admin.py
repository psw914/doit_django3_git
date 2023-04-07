from django.contrib import admin
from blog import models

# Register your models here.
admin.site.register(models.Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag,TagAdmin)