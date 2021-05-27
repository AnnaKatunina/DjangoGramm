from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

from app_DjangoGramm.models import User, Profile, Post


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'h6 font-weight-light'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'username',
                'email',
                'password1',
                'password2',
            ),
            ButtonHolder(
                Submit('submit', 'Sign up', css_class='btn btn-primary btn-lg btn-block'),
            ),
        )


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'text-muted'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'username',
                'password',
            ),
            ButtonHolder(
                Submit('submit', 'Sign in', css_class='btn btn-primary btn-lg btn-block'),
            ),
        )


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('avatar', 'full_name', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'text-muted'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'avatar',
                'full_name',
                'bio'
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary btn-lg'),
            ),
        )


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'text-muted'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'image',
                'description',
            ),
            ButtonHolder(
                Submit('submit', 'Post', css_class='btn btn-primary btn-lg'),
            ),
        )
