from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

#-----Announcement Section-----#

class Announcement(models.Model):
    announcement_list = models.CharField(max_length=1000,null=True)
    pub_date = models.DateTimeField(default=now)
    image_announcement= models.ImageField(upload_to='media/images/', null=True, blank=True)
    document_announcement = models.FileField(upload_to='media/documents/', null=True, blank=True)

    def __str__(self):
        return f"Announcement {self.id}"

class Recommendation(models.Model):
    recommendation_list = models.CharField(max_length=1000, null=True)
    pub_date = models.DateTimeField(default=now)
    image_recommendation = models.ImageField(upload_to='media/images/', null=True, blank=True)
    document_recommendation = models.FileField(upload_to='media/documents/', null=True, blank=True)

    def __str__(self):
        return f"Recommendation {self.id}"

#-----Announcement Section/end-----#




#-----Records Table-----#



#-----Records Table/end-----#


class intern(AbstractUser):
    student_id = models.CharField(max_length=200, verbose_name='Student ID', null=True)
    course = models.CharField(max_length=200, verbose_name='Course', null=True)
    company_name = models.CharField(max_length=200, verbose_name='Company', null=True)
    contact_num = models.CharField(max_length=200, verbose_name='Contact Number', null=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='images/default_profile_image.png')
    pub_date = models.DateTimeField(default=now)
    # Intern Status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('excused', 'Excused'),
        ('absent', 'Absent'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)

    @property
    def status_color(self):
        if self.status == 'active':
            return 'green'
        elif self.status == 'excused':
            return 'yellow'
        elif self.status == 'absent':
            return 'red'
    pass

    def __str__(self):
        return self.username

#-----Time Record-----#

class TimeRecord(models.Model):
    intern_user = models.ForeignKey(intern, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(default=now)
    is_time_in = models.BooleanField(default=True)
    action = models.CharField(max_length=8, choices=[('Time In', 'Time In'), ('Time Out', 'Time Out')], default='Time In')
#-----Time Record/end-----#

#-----CalendarSetup-----#


class InternshipCalendar(models.Model):
    user = models.ForeignKey(intern, on_delete=models.CASCADE)
    starting_month = models.IntegerField()
    starting_date = models.IntegerField()
    ending_month = models.IntegerField()
    ending_date = models.IntegerField()
    weekly_workshift = models.CharField(max_length=100)
    timeshift = models.CharField(max_length=100)
    rest_days = models.CharField(max_length=100)

    def __str__(self):
        return f"Calendar for {self.user}"
#-----CalendarSetup/end-----#

class InternsCalendar(models.Model):
    user = models.ForeignKey(intern, on_delete=models.CASCADE)
    start_month = models.DateField()
    end_month = models.DateField()
    num_submission_bins = models.PositiveIntegerField(default=0)  # Default value of 0

    def update_num_submission_bins(self):
        # Calculate and update the number of submission bins
        self.num_submission_bins = (self.end_month - self.start_month).days + 1

    def save(self, *args, **kwargs):
        self.update_num_submission_bins()  # Update num_submission_bins before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"InternsCalendar for {self.user}"

class DailyAccomplishment(models.Model):
    interns_calendar = models.ForeignKey(InternsCalendar, on_delete=models.CASCADE)
    date = models.DateField()
    text_submission = models.TextField()
    document_submission = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"Accomplishment for {self.interns_calendar.user} on {self.date}"


