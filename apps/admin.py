from django.contrib.admin import ModelAdmin, register, StackedInline

from apps.models import Course, Teacher


# Register your models here.
@register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('name', 'description', 'list_image', 'detail_image', 'detail_video')


@register(Teacher)
class TeacherModelAdmin(ModelAdmin):
    list_display = ('full_name', 'job_field', 'image', 'video')

# @register(CourseImage)
# class CourseImageModelAdmin(ModelAdmin):
#     pass
