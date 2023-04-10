from django.contrib import admin
from blog import models


#summernote
from django_summernote.admin import SummernoteModelAdmin


# Apply summernote to all TextField in model.
# class PostAdmin(SummernoteModelAdmin):  
# class SomeModelAdmin(SummernoteModelAdmin):  
#     summernote_fields = '__all__'
#     # summernote_fields = ('content',)

# admin.site.register(models.Post, SomeModelAdmin)

class PostAdmin(SummernoteModelAdmin):
    # summernote_fields = ('content',)
    summernote_fields = '__all__'

admin.site.register(models.Post, PostAdmin)



# Register your models here.
# admin.site.register(models.Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag,TagAdmin)