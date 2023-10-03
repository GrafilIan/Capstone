from django import forms
from .models import intern, Announcement, Recommendation, InternshipCalendar
from .models import InternsCalendar, DailyAccomplishment, TimeRecord

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

class InternshipCalendarForm(forms.ModelForm):
    class Meta:
        model = InternshipCalendar
        exclude = ['user']

class InternsCalendarForm(forms.ModelForm):
    class Meta:
        model = InternsCalendar
        fields = ['start_month', 'end_month']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.update_num_submission_bins()  # Update num_submission_bins before saving
        if commit:
            instance.save()
        return instance

class DailyAccomplishmentForm(forms.ModelForm):
    class Meta:
        model = DailyAccomplishment
        fields = ['date', 'text_submission', 'document_submission']

    def __init__(self, *args, **kwargs):
        super(DailyAccomplishmentForm, self).__init__(*args, **kwargs)
        self.fields['text_submission'].required = False