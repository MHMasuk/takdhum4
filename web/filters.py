from .models import Course
import django_filters


class CourseFilter(django_filters.FilterSet):
    course_title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ('course_title',)


class SearchForm():
    pass