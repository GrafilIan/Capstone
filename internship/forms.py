from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import intern, Announcement, Recommendation, InternshipCalendar
from .models import DailyAccomplishment
from .models import InternsCalendar
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = intern
        fields = ("username", "email", "student_id", "course", "company_name", "contact_num", "address", "profile_image")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = intern
        fields = ("username", "email", "student_id", "course", "company_name", "contact_num", "address", "profile_image")


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['announcement_list', 'image_announcement', 'document_announcement']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['announcement_list'].required = False

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['recommendation_list', 'image_recommendation', 'document_recommendation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recommendation_list'].required = False


class TimeRecordForm(forms.Form):
    is_time_in = forms.BooleanField(required=True, widget=forms.HiddenInput())

class   InternshipCalendarForm(forms.ModelForm):
    class Meta:
        model = InternshipCalendar
        exclude = ['user']

class InternsCalendarForm(forms.ModelForm):
    class Meta:
        model = InternsCalendar
        fields = ['start_date', 'end_date']

class DailyAccomplishmentForm(forms.ModelForm):
    class Meta:
        model = DailyAccomplishment
        fields = ['date', 'text_submission', 'document_submission']


