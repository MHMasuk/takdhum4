from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from web.models import Profile, UserMessage, Subcribe, Question, StudentAnswer


class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"UserID", 'value':""}))
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"e-mail", 'value':""}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'value':''}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password', 'value':''}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserMessageForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.Textarea()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'col-sm-6'


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('slug', 'user')


class ContactForm(forms.ModelForm):

    class Meta:
        model = UserMessage
        fields = '__all__'


class SubcriberForm(forms.ModelForm):

    class Meta:
        model = Subcribe
        fields = '__all__'


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('option1', 'option2', 'option3', 'option4')


class AnswerForm(forms.ModelForm):

    class Meta:
        model = StudentAnswer
        fields = ('answer_file',)

