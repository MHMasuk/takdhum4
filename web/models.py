from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    profile_picture = models.ImageField(upload_to='Profile_picture/', null=True, blank=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def get_absulete_url(self):
        return reverse('user_profile', args=[str(self.slug)])


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


class CourseCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_url = models.CharField(max_length=50)
    thumbnail_image = models.ImageField(upload_to='Course_Category', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name


class CourseLevel(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_title = models.CharField(max_length=150)
    course_url = models.CharField(max_length=150)
    thumbnail_image = models.ImageField(upload_to='Courses')
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    course_level = models.ForeignKey(CourseLevel, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.course_title


class TakenCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taken_courses')
    taken_course_title = models.CharField(max_length=255, null=True)
    taken_course_url = models.CharField(max_length=255, null=True)
    taken_course_image = models.ImageField(upload_to='User/TakenCourses', null=True)
    taken_course_category = models.CharField(max_length=255, null=True)
    taken_category_url = models.CharField(max_length=255, null=True)
    view = models.PositiveIntegerField(blank=True, null=True)
    taken_time = models.DateTimeField(auto_now=True)
    last_visited = models.DateTimeField()

    class Meta:
        unique_together = (('user', 'taken_course_url'),)

    def get_absolute_url(self):
        return reverse('my_course', kwargs={'pk': self.pk})

    def __str__(self):
        return self.taken_course_url


class SingleVideo(models.Model):
    video_title = models.CharField(max_length=150)
    video_url = models.CharField(max_length=150)
    video_link = models.URLField()
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.video_title


class AboutUs(models.Model):
    our_journey = models.TextField()
    our_history_and_passions = models.TextField(blank=True, null=True)
    about_image = models.ImageField(upload_to='About us')

    def __str__(self):
        return self.our_journey


class Basic_info(models.Model):
    name = models.CharField(max_length=100)
    slogan = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='About us')
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    office_address = models.TextField()
    promo_video = models.URLField(blank=True, null=True)
    google_map_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    google_plus_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Slider(models.Model):
    small_text = models.CharField(max_length=100, null=True, blank=True)
    big_text = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=250)
    slide_image = models.ImageField(upload_to='Slider_Image')

    def __str__(self):
        return self.big_text


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    date_and_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.question


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.CharField(max_length=3)
    month = models.CharField(max_length=10)
    start_and_end_time = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Events')
    gallery_image1 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image2 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image3 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image4 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image5 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image6 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image7 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image8 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image9 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image10 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image11 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    gallery_image12 = models.FileField(blank=True, null=True, upload_to='Gallery/events')
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    Image = models.ImageField(upload_to='Projects')
    upload_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    person_name = models.CharField(max_length=100)
    person_designation = models.CharField(max_length=100)
    person_comment = models.TextField()
    person_image = models.ImageField(upload_to='Testimonial')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.person_name


class UserMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.first_name + self.last_name


class Subcribe(models.Model):
    subcriber_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subcriber_email


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField('Question', max_length=400)
    question_file = models.FileField('Question', upload_to='Question-file', blank=True, null=True)
    option1 = models.CharField(max_length=50, blank=True, null=True)
    option2 = models.CharField(max_length=50, blank=True, null=True)
    option3 = models.CharField(max_length=50, blank=True, null=True)
    option4 = models.CharField(max_length=50, blank=True, null=True)
    correct_answer = models.CharField(max_length=25, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class StudentAnswer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    answer_file = models.FileField(upload_to='Student-answer', blank=True, null=True)
    answer_text = models.CharField(max_length=255, blank=True, null=True)
    counter = models.PositiveIntegerField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    is_pass = models.BooleanField(default=False)

    def __str__(self):
        return self.student.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taken_quizzes')
    date = models.DateTimeField(auto_now_add=True)


class WatchVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    course = models.ForeignKey(TakenCourse, on_delete=models.CASCADE, related_name='watch_video')
    # course_title = models.CharField(TakenCourse, on_delete=models.CASCADE, related_name='watch_video')
    vedio = models.ForeignKey(SingleVideo, on_delete=models.CASCADE)
    # vedio = models.CharField(max_length=300)
    view = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.vedio.video_title
