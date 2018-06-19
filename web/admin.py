from django.contrib import admin
from .models import *


# Register your models here.
class SingleVideoModelAdmin(admin.ModelAdmin):
    list_display = ['video_title', 'video_link', 'course_name', 'is_public']
    list_display_links = ['video_title', 'video_link']
    # list_editable = ['video_link']
    list_filter = ['course_name', 'is_public']
    search_fields = ['video_title', 'course_name']

    class Meta:
        model = SingleVideo


admin.site.register(SingleVideo, SingleVideoModelAdmin)


class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['course_title', 'course_category', 'description']
    list_display_links = ['course_title']
    # list_editable = ['description']
    list_filter = ['course_category', 'course_level']
    search_fields = ['course_title', 'course_category', 'description']

    class Meta:
        model = Course


admin.site.register(Course, CourseModelAdmin)

admin.site.register(CourseLevel)


admin.site.register(CourseCategory)

admin.site.register(FAQ)

admin.site.register(AboutUs)


class BasicInfoModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_1', 'email', 'office_address']
    list_display_links = ['name', 'phone_1', 'email', 'office_address']
    # list_editable = ['phone_1', 'email', 'office_address']

    class Meta:
        model = Basic_info


admin.site.register(Basic_info, BasicInfoModelAdmin)

admin.site.register(Slider)

admin.site.register(Event)

admin.site.register(Project)

admin.site.register(Testimonial)

admin.site.register(UserMessage)

admin.site.register(Profile)

admin.site.register(Subcribe)
admin.site.register(TakenCourse)
admin.site.register(Question)
admin.site.register(StudentAnswer)
admin.site.register(WatchVideo)

