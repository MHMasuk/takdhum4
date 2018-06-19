from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from web.filters import CourseFilter
from django.core.mail import send_mail
from .models import CourseCategory, Basic_info, Slider, Course, Event, Project, CourseLevel, SingleVideo, Testimonial, \
    AboutUs, FAQ, UserMessage, Profile, TakenCourse, Question, TakenQuiz, StudentAnswer, WatchVideo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignupForm, UserMessageForm, UserForm, ProfileForm, ContactForm, SubcriberForm, QuestionForm, \
    AnswerForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import requests



def index(request):
    """Takdhum home page"""
    # Need for all view
    categories = CourseCategory.objects.all()
    basic_info = Basic_info.objects.first()

    sliders = Slider.objects.all()
    courses = Course.objects.all()[::-1]
    events = Event.objects.all().order_by('-upload_time')
    if len(events) > 3:
        events = events[0:3]
    projects = Project.objects.all().order_by('-upload_time')
    testimonials = Testimonial.objects.last()

    if request.method == 'POST':
        form = SubcriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully subscribe in Takdhum.')
    else:
        form = SubcriberForm()
    context = {
        'categories': categories,
        'slides': sliders,
        's': courses,
        'info': basic_info,
        'events': events,
        'projects': projects,
        't': testimonials,
        'form': form,
    }
    return render(request, 'takdhum/index.html', context)


def subscriber(request):
    if request.method == 'POST':
        form = SubcriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully subscribe in Takdhum.')
            return redirect('index')
        else:
            messages.error(request, 'Something Wrong!! Please try again.')
            return redirect('index')
    else:
        form = SubcriberForm()


class ProfilePage(generic.DetailView, LoginRequiredMixin):
    model = User
    slug_field = 'username'
    template_name = 'takdhum/profile/user_profile.html'
    redirect_field_name = 'sign-up'

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
        context['info'] = Basic_info.objects.first()
        context['categories'] = CourseCategory.objects.all()
        return context


@login_required
@transaction.atomic
def update_profile(request):
    categories = CourseCategory.objects.all()
    basic_info = Basic_info.objects.first()
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            user = request.user
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user_profile', request.user)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'takdhum/profile/profile_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'info': basic_info,
        'categories': categories,
        'title': 'Update Profile',
    })


def drawing_course(request, category, level):
    categories = CourseCategory.objects.all()
    basic_info = Basic_info.objects.first()

    levels = CourseLevel.objects.all()
    course_level = get_object_or_404(CourseLevel, url=level)
    requested_category = get_object_or_404(CourseCategory, category_url=category)
    requested_category_course = Course.objects.filter(course_category=requested_category.id).filter(course_level=course_level.id).order_by('course_title')

    # courses = get_object_or_404(CourseCategory, category_url=category)

    context = {
        'categories': categories,
        # 'course_level': course_level,
        'level': levels,
        'info': basic_info,
        'tag': category,
        'heading': requested_category.category_name + ' ' + course_level.name,
        'courses': requested_category_course,
        'title': requested_category.category_name,
    }
    return render(request, 'takdhum/course_category.html', context)


def courseCategory(request, category=None):
    """Takdhum All course category, resent course, popular course etc."""
    # Need for all view
    categories = CourseCategory.objects.all()
    basic_info = Basic_info.objects.first()

    level = CourseLevel.objects.all()

    requested_category = get_object_or_404(CourseCategory, category_url=category)
    requested_category_course = Course.objects.filter(course_category=requested_category.id).order_by('course_title')

    # courses = get_object_or_404(CourseCategory, category_url=category)

    context = {
        'categories': categories,
        'level': level,
        'info': basic_info,
        'tag': category,
        'courses': requested_category_course,
        'title': requested_category.category_name,
    }
    if category == 'drawing':
        return render(request, 'takdhum/course_category.html', context)
    else:
        return render(request, 'takdhum/all_course.html', context)


def course(request, category, course):

    """All takdhum single course display here"""

    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()
    course_category = get_object_or_404(CourseCategory, category_url=category)
    single_course = get_object_or_404(Course, course_url=course)
    allCourses = Course.objects.exclude(course_url=single_course.id).filter(course_category=course_category.id).order_by('course_title')
    course_videos = SingleVideo.objects.filter(course_name=single_course.id)
    all_videos = SingleVideo.objects.all()
    print('vedio', request.POST.get('vedio_name'))

    if request.user.is_active:
        try:
            courses = TakenCourse()
            courses.user = request.user
            courses.taken_course_url = single_course.course_url
            courses.taken_course_title = single_course.course_title
            courses.taken_course_image = single_course.thumbnail_image
            courses.taken_course_category = course_category.category_name
            courses.taken_category_url = course_category.category_url
            courses.last_visited = timezone.now()
            courses.save()
        except:
            pass
    try:
        if request.user.is_authenticated:
            taken_course = get_object_or_404(TakenCourse, taken_course_url=course, user=request.user)
            print(taken_course)
            course_videos = SingleVideo.objects.filter(course_name=single_course.id)
            total_vedios = course_videos.count()
            print(total_vedios)

            watch_video = WatchVideo.objects.filter(course=taken_course.id, user=request.user)
            print(watch_video.count())
            total_unwatch_vedios = total_vedios - watch_video.count()
            progress = 100 - round((total_unwatch_vedios / total_vedios) * 100)
            print('Progress', progress)
            # except:
            #     pass
            context = {
                'categories': categories,
                'course_name': single_course,
                'course_videos': course_videos,
                'all_Courses': allCourses,
                'all_videos': all_videos,
                'request_category': category,
                'info': basic_info,
                'title': course,
                'progress': progress,
            }
            return render(request, 'takdhum/single_course.html', context)
    except:
            context = {
                'categories': categories,
                'course_name': single_course,
                'course_videos': course_videos,
                'all_Courses': allCourses,
                'all_videos': all_videos,
                'request_category': category,
                'info': basic_info,
                'title': course,
            }
            return render(request, 'takdhum/single_course.html', context)


def my_course(request, user=None):
    if request.user.is_authenticated:
        basic_info = Basic_info.objects.first()
        categories = CourseCategory.objects.all()
        login_user = get_object_or_404(User, username=user)
        user_course_list = TakenCourse.objects.filter(user=login_user.id)
        watch = user_course_list.filter(watch_video__user=login_user.id)
        print(watch)

        user_profile = get_object_or_404(Profile, user=login_user.id)
        #print(watch_video)

        context = {
            'info': basic_info,
            'categories': categories,
            'title': login_user.username + ' course list',
            'user_course_list': user_course_list.order_by('-taken_time'),
        }
        return render(request, 'takdhum/profile/my_course.html', context)


def all_course(request):
    """Show takddhum all courses"""
    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    level = CourseLevel.objects.all()
    courses = Course.objects.all().order_by('course_title')

    context = {
        'categories': categories,
        'level': level,
        'courses': courses,
        'info': basic_info,
        'tag': 'All',
        'title': 'All courses',
    }
    return render(request, 'takdhum/all_course.html', context)


def popular_course(request):
    """Show takdhum popular courses"""
    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    level = CourseLevel.objects.all()
    courses = Course.objects.all().order_by('course_title')

    context = {
        'categories': categories,
        'level': level,
        'courses': courses,
        'info': basic_info,
        'tag': 'Popular',
        'title': 'Takdhum Popular Courses'
    }
    return render(request, 'takdhum/all_course.html', context)


def recent_course(request):
    """Show takdhum recent courses"""
    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    level = CourseLevel.objects.all()
    courses = Course.objects.all().order_by('course_title')[::-1]

    context = {
        'categories': categories,
        'level': level,
        'courses': courses,
        'info': basic_info,
        'tag': 'Recent',
        'title': 'Takdhum Recent Courses'
    }
    return render(request, 'takdhum/all_course.html', context)


def event(request, event_id):
    """Takdhum single event page"""
    # Need for all view
    categories = CourseCategory.objects.all()
    basic_info = Basic_info.objects.first()

    requested_event = get_object_or_404(Event, id=event_id)

    context = {
        'categories': categories,
        'info': basic_info,
        'single_event': requested_event,
        'title': requested_event.title,
    }
    return render(request, 'takdhum/single_event.html', context)


def about_us(request):
    """Takdhum about us page"""
    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    about = AboutUs.objects.first()
    context = {
        'info': basic_info,
        'categories': categories,
        'about': about,

    }
    return render(request, 'takdhum/about_us.html', context)


def contact(request):
    """Takdhum contact page"""
    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You message send successfully.')
            redirect('contact_page')
        else:
            messages.error(request, 'Please try again!.')
            redirect('contact_page')
    else:
        form = ContactForm()
    context = {
        'info': basic_info,
        'categories': categories,
        'form': form,
        'title': 'Contact',
    }
    return render(request, 'takdhum/contact.html', context)


def user_message(request):
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    context = {
        'info': basic_info,
        'categories': categories,
    }
    if request.method == 'POST':
        form = UserMessageForm(request.POST or None)
        if form.is_valid():
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            message = request.POST.get('contact-message', '')
            user_message_obj = UserMessage(first_name=first_name, last_name=last_name, email=email, message=message)
            user_message_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Message sent successfully!')
    else:
        messages.add_message(request, messages.ERROR, 'Something went wrong!')

    return render(request, 'takdhum/contact.html', context)


def faq(request):
    """Takdhum FAQ page"""
    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    question_ans = FAQ.objects.all()
    context = {
        'info': basic_info,
        'categories': categories,
        'faq': question_ans,
    }
    return render(request, 'takdhum/faq.html', context)


def get_user_profile(request, username=None):
    if request.user.is_authenticated:
        basic_info = Basic_info.objects.first()
        categories = CourseCategory.objects.all()
        login_user = get_object_or_404(User, username=username)
        if not login_user:
            return redirect('index')
        # print(login_user)
        context = {
            'info': basic_info,
            'categories': categories,
            'title': 'Profile',
        }
        return render(request, 'takdhum/profile/user_profile.html', context)
    else:
        return redirect('get_login')


def get_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        basic_info = Basic_info.objects.first()
        categories = CourseCategory.objects.all()
        form = SignupForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('get_login')

        context = {
            'categories': categories,
            'info': basic_info,
            'form': form,
            'title': 'Login'
        }
        if request.method == 'POST':
            user = request.POST.get('username')
            password = request.POST.get('password')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                # messages.add_message(request, messages.ERROR, 'Login Successful')
                # return redirect('profile')
                return redirect('user_profile', username=request.user)
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password Wrong!')
                return redirect('get_login')
    return render(request, 'takdhum/login-reg.html', context)


def get_logout(request):
    logout(request)
    return redirect('index')


def signup(request):
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            c_pass = form.cleaned_data.get('password2')
            print(c_pass)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Takdhum account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'password': c_pass,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            context = {
                'info': basic_info,
                'categories': categories,
                'form': form,
                'title': 'Sign up'
            }
            return render(request, 'takdhum/activation_message.html', context)
            # return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    context = {
        'info': basic_info,
        'categories': categories,
        'form': form,
        'title': 'Sign up'
    }

    return render(request, 'takdhum/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user_profile', request.user)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        # return HttpResponse('Your account will be activate within 6 hours.')
        return HttpResponse('Activation link is invalid!')


def get_sign_up(request):
    if request.user.is_authenticated:
        return redirect('get_login')
    else:
        form = SignupForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.INFO, 'Registration Successfully Completed!')
            return redirect('get_login')
        basic_info = Basic_info.objects.first()
        categories = CourseCategory.objects.all()
        context = {
            'info': basic_info,
            'categories': categories,
            'form': form,
            'title': 'Sign up'
        }
        return render(request, 'takdhum/register.html', context)


class EventListView(generic.ListView):
    template_name = 'takdhum/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all().order_by('-upload_time')

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context['info'] = Basic_info.objects.first()
        context['categories'] = CourseCategory.objects.all()
        return context


def search(request):
    course_list = Course.objects.all()
    course_filter = CourseFilter(request.GET, queryset=course_list)

    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()
    return render(request, 'takdhum/search/course_list.html', {'filter': course_filter,
                                                               'info': basic_info,
                                                               'categories': categories})


@login_required
def taken_course_delete(request, user, pk):
    try:
        instance1 = TakenCourse.objects.get(pk=pk)
        delete_course = instance1.taken_course_title
        instance1.delete()
        messages.warning(request, f'{delete_course} course is remove form your taken course.')
        return redirect('my_course', user=request.user)
    except:
        return redirect('my_course', user=request.user)


def take_quiz(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuestionForm()
    return render(request, 'quiz/taken_quiz_form.html', {'form': form})


def question_list(request, course):
    student_name = request.user
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    single_course = get_object_or_404(Course, course_url=course)
    question = Question.objects.filter(course=single_course.id)
    cou = Course.objects.filter(course_url=course)
    print('Something', cou)
    print(question.filter())
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Your answer submitted successfully.')
            return redirect('question-list', course)
    else:
        form = AnswerForm()
    return render(request, 'quiz/taken_quiz_list2.html', {'question_list': question,
                                                          'form': form})


def student_answer(request, username):
    answer_list = StudentAnswer.objects.filter(student__username=username)\
        .values_list('course__course_title', flat=True).distinct()

    score = StudentAnswer.objects.filter(student__username=username, is_pass=True).count()

    context = {
        'studentanswer_list': answer_list,
        'score': score
    }
    return render(request, 'takdhum/profile/my_taken_course.html', context)


def score(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # s_answer = get_object_or_404(StudentAnswer, question=question_id)
    # print(s_answer)
    if request.POST.get('question'):

        exist = StudentAnswer.objects.filter(student=request.user,
                                             course__course_title=question.course.course_title,
                                             question=question.pk).exists()
        print(exist)

        if exist:
            messages.warning(request, 'You already answer this question')
            return redirect('question-list', course=question.course.course_url)
        else:
            a_file = question.question_file
            user = request.user
            c_title = question.course.course_title
            q = question.question
            a_text = request.POST.get('question')
            # answer_counter = s_answer.counter
            if question.correct_answer == a_text:
                instance = StudentAnswer.objects.create(student=user, answer_text=a_text,
                                         question=question, course=question.course, counter=1)
                instance.save()
                print(StudentAnswer.counter)
            messages.success(request, 'Your answer is submitted')
            return redirect('question-list', course=question.course.course_url)
    else:
        user = request.user
        q = question.question
        if request.method == 'POST':
            form = AnswerForm(request.POST, request.FILES)

            exist = StudentAnswer.objects.filter(student=request.user,
                                                 course__course_title=question.course.course_title,
                                                 question=question.pk).exists()
            if exist:
                messages.warning(request, 'You already answer this question')
                return redirect('question-list', course=question.course.course_url)
            else:
                if form.is_valid():
                    form = form.save(commit=False)
                    form.student = user
                    form.course = question.course
                    form.question = question
                    form.save()
                    messages.success(request, 'Your answer submitted successfully.')
                    return redirect('question-list', course=question.course.course_url)
        else:
            form = AnswerForm()
        return redirect('question-list', course=question.course.course_url)


def email_send(request):
    to_email = request.email
    send_mail('Takdhum quiz answer', 'Message body', 'info.takdhum@gmail.com', ['m.h.masukboss@gmail.com'])
    messages.success(request, 'Email sent successfully')


class AllAnswer(generic.ListView):
    model = StudentAnswer
    template_name = 'quiz/student_answer.html'


def quize_details(request):

    a = request.POST.get('q')
    print("course: ", a)

    course = Course.objects.get(course_title=a)

    question = Question.objects.filter(course=course.id).count()

    answer = StudentAnswer.objects.filter(student=request.user, course__course_title=a).count()

    score = StudentAnswer.objects.filter(student=request.user, course__course_title=a, counter=1).count()

    context = {
        'question': question,
        'course': course,
        'answer': answer,
        "score": score,

    }
    return render(request, 'takdhum/profile/quize_details.html', context)


# def course_vedio(request):

def vedio_link(request):
    print(request.POST.get('vedio_name'))


class SingleVedioView(generic.DetailView):
    model = SingleVideo
    template_name = 'takdhum/single_vedio.html'

    def get_context_data(self, **kwargs):
        context = super(SingleVedioView, self).get_context_data(**kwargs)
        context['info'] = Basic_info.objects.first()
        context['categories'] = CourseCategory.objects.all()
        #context['course_videos'] = get_object_or_404(SingleVideo, pk=SingleVideo.pk)
        return context


def single_video(request, category, course, video):
    """All takdhum single course display here"""
    # Need for all view
    basic_info = Basic_info.objects.first()
    categories = CourseCategory.objects.all()

    course_category = get_object_or_404(CourseCategory, category_url=category)
    single_course = get_object_or_404(Course, course_url=course)
    taken_course = get_object_or_404(TakenCourse, taken_course_url=course, user=request.user)
    print(taken_course)
    allCourses = Course.objects.exclude(course_url=single_course.id).filter(course_category=course_category.id).order_by('course_title')
    course_videos = SingleVideo.objects.filter(course_name=single_course.id)
    total_vedios = course_videos.count()
    print(total_vedios)
    # single_vedio = SingleVideo.objects.get(video_url__exact=video)
    single_vedio = SingleVideo.objects.get(video_title__exact=video)
    print(single_vedio)
    all_videos = SingleVideo.objects.all()

    if request.user.is_active:
        print(request.user)
        try:
            exist = WatchVideo.objects.filter(user=request.user, category=course_category,
                                              course=taken_course, vedio=single_vedio).exists()
            print(exist)
            if exist:
                pass
            else:
                WatchVideo.objects.create(user=request.user, category=course_category,
                                          course=taken_course, vedio=single_vedio)
        except:
            pass
    watch_video = WatchVideo.objects.filter(course=taken_course.id, user=request.user)
    print(watch_video.count())
    total_unwatch_vedios = total_vedios - watch_video.count()
    progress = 100 - round((total_unwatch_vedios / total_vedios) * 100)
    print(progress)

    context = {
        'categories': categories,
        'course_name': single_course,
        'course_videos': course_videos,
        'all_Courses': allCourses,
        'all_videos': all_videos,
        'request_category': category,
        'info': basic_info,
        'title': course,
        'single_video': single_vedio,
        'progress': progress,
    }
    return render(request, 'takdhum/single_vedio.html', context)


def watch_vedio(request, course_watch):
    #courses = Course.objects.filter(course_url=course_watch)
    taken_course = TakenCourse.objects.filter(taken_course_title=course_watch)
    print(taken_course)
    watch = WatchVideo.objects.filter(course__taken_course_url=course_watch)
    print(watch)
    course = Course.objects.filter()
    print(course)

    context = {
        #'course': course,
        'watch': watch,
    }
    return render(request, 'takdhum/profile/watch_vedio.html', context)
