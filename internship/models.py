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
    timestamp = models.DateTimeField(default=now)
    is_time_in = models.BooleanField(default=True)

#-----Time Record/end-----#


