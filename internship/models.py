from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

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
    middle_name = models.CharField(max_length=200, verbose_name='Middle Name', null=True)
    suffix = models.CharField(max_length=200, verbose_name='suffix', null=True)
    course = models.CharField(max_length=200, verbose_name='Course', null=True)
    company_name = models.CharField(max_length=200, verbose_name='Company', null=True)
    position = models.CharField(max_length=200, verbose_name='Position', null=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='images/default_profile_image.png')
    pub_date = models.DateTimeField(default=now)
    timezone = models.CharField(max_length=63, default='Asia/Manila')
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
    start_week_number = models.PositiveIntegerField(null=True)
    num_submission_bins = models.PositiveIntegerField(default=0)  # Default value of 0

    def update_num_submission_bins(self):
        # Calculate and update the number of submission bins
        self.num_submission_bins = (self.end_month - self.start_month).days + 1

    def save(self, *args, **kwargs):
        self.update_num_submission_bins()  # Update num_submission_bins before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"InternsCalendar for {self.user}"

class TimeRecord(models.Model):
    interns_calendar = models.ForeignKey(InternsCalendar, on_delete=models.CASCADE, default=None)
    intern_user = models.ForeignKey(intern, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_time_in = models.BooleanField(default=False)
    action = models.CharField(max_length=8, choices=[('Time In', 'Time In'), ('Time Out', 'Time Out')], default='Time In')
    date = models.DateField(null=True)

    def __str__(self):
        return f"TimeRecord for {self.interns_calendar}"


class DailyAccomplishment(models.Model):
    interns_calendar = models.ForeignKey(InternsCalendar, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(intern, on_delete=models.CASCADE, default=1)
    date = models.DateField(null=True)
    is_rest_day = models.BooleanField(default=False)
    text_submission = models.TextField()
    hours_submission = models.TextField(null=True)
    document_submission = models.FileField(upload_to='documents/',null=True, blank=True)


    def __str__(self):
        return f"Accomplishment for {self.interns_calendar.user} on {self.date}"


### For Uploading Requirements ###

class Document(models.Model):
    REQUIREMENT_CHOICES = [
        ('Acceptance Form for OJT', 'Acceptance Form for OJT'),
        ('Internship Agreement', 'Internship Agreement'),
        ('Merit of Rating', 'Merit of Rating'),
        ('Student INFO Sheet', 'Student INFO Sheet'),
        ('Supervisor Feedback Form', 'Supervisor Feedback Form'),
        ('Student Feedback Form', 'Student Feedback Form'),
        ('Parent Consent', 'Parent Consent'),
        ('Barangay Clearance', 'Barangay Clearance'),
        ('Police Clearance', 'Police Clearance'),
        ('Parent ID', 'Parent ID'),
        ('Medical Certificate', 'Medical Certificate'),
        ('Cedula', 'Cedula'),
        # Add more choices as needed
    ]

    user = models.ForeignKey(intern, on_delete=models.CASCADE)
    requirement = models.CharField(max_length=100, choices=REQUIREMENT_CHOICES)
    document_image = models.ImageField(upload_to='documents/')

    def __str__(self):
        return f"{self.requirement} - {self.id}"

### End ###
