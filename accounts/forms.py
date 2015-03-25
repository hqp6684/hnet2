from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile, Patient, Employee
from django.forms.models import model_to_dict, fields_for_model
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from localflavor.us.forms import USSocialSecurityNumberField, USPhoneNumberField  
class UserCreationForm(forms.ModelForm):

    #error_css_class = 'alert-danger'
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")},
        widget=forms.TextInput(attrs={'class':'form-control'}),

        )


    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    sSN = USSocialSecurityNumberField(label=_("SSN"), 
        widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=11,)
    phoneNumber = USPhoneNumberField(label=_("Phone"),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=15,)

    class Meta:
        model = UserProfile
        exclude = ['user', 'ref_id',]

        fields =['fName', 'lName', 'mName', 'dOB', 'sSN',
        'phoneNumber','streetAddress','city','state',
        'zipcode','email',]
        widgets = {
            'fName' : forms.TextInput(attrs={'class':'form-control'}),
            'lName' : forms.TextInput(attrs={'class':'form-control'}),
            'mName' : forms.TextInput(attrs={'class':'form-control'}),
            'dOB' : forms.DateInput(attrs={'class':'datepicker form-control'}),
            'streetAddress' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            'state' : forms.Select(attrs={'class': 'form-control'}),
            'zipcode' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
        }



#create a new patient
class NewPatientForm(forms.ModelForm):
    class Meta:
        model = Patient



class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['employee']
        fields= ['employee_type']



#login form from Django auth forms
class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    username = forms.CharField(label=_("Username"),
        max_length=254,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username', 'required': True, 'autofocus':True}))
    password = forms.CharField(label=_("Password"), 
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password','required': True}))

    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
