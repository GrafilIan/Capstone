from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import AnnouncementForm, RecommendationForm
from .models import Announcement, Recommendation, intern, TimeRecord, WeeklyReport
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import InternsCalendar, DailyAccomplishment
from .models import Document
from datetime import timedelta
from django.utils.timezone import now
from django import forms
from django.http import HttpResponse
from datetime import date
from .forms import DailyAccomplishmentForm, TimeRecordForm
from django.utils import timezone
import pytz
from django.http import JsonResponse
from django.contrib import messages
###-----------------------------------Login-------------------------------------###



def InternRegister(request):
    if request.method == 'POST':
        # Get the data from the POST request
        username = request.POST['username']
        password1 = request.POST['password1']  # Use 'password1' to retrieve the first password input
        password2 = request.POST['password2']
        email = request.POST['email']
        student_id = request.POST['student_id']
        middle_name = request.POST['middle_name']
        suffix = request.POST['suffix']
        course = request.POST['course']
        company_name = request.POST['company_name']
        position = request.POST['position']
        address = request.POST['address']
        profile_image = request.FILES.get('profile_image')

        if password1 != password2:
            # Handle password mismatch error (e.g., return an error response or render a form with an error message)
            return render(request, 'registration/InternRegister.html', {'error_message': 'Passwords do not match'})

        # Create a new intern object and save it to the database
        intern_obj = intern(
            username=username,
            email=email,
            student_id=student_id,
            middle_name=middle_name,
            suffix=suffix,
            course=course,
            company_name=company_name,
            position=position,
            address=address,
            profile_image=profile_image,
            pub_date=now()
        )
        intern_obj.set_password(password1)
        intern_obj.save()

        # Log in the user
        login(request, intern_obj)

        # Redirect to a success page or profile page
        return redirect('Login')  # Change 'profile' to your desired URL

    return render(request, 'registration/InternRegister.html')

def loginnn(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            # Extract username and password from the form
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')

            # Use authenticate to check credentials
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if user.is_superuser:
                    # Superuser, redirect to some other page for superusers
                    return redirect('time_in_out')  # Replace 'superuser_dashboard' with your desired URL name

                # Check if the user has calendar records
                has_calendars = InternsCalendar.objects.filter(user=request.user).exists()

                if has_calendars:
                    # User has calendars, redirect to view_calendar
                    return redirect('calendar_view')
                else:
                    # User doesn't have calendars, check the session variable
                    if request.session.get('redirect_to_create_calendar'):
                        messages.info(request, 'Please set up your calendar.')
                        del request.session['redirect_to_create_calendar']  # Remove the session variable
                        return redirect('interns_calendar_create')
                    else:
                        # No session variable, redirect to some other page
                        return redirect('interns_calendar_create')
            else:
                # Authentication failed for wrong password
                messages.error(request, 'Incorrect password. Please try again.')

    else:
        auth_form = AuthenticationForm()

    return render(request, 'Login.html', {'auth_form': auth_form})

@login_required
def redirect_to_calendar(request):
    # Check if the user has calendar records
    has_calendars = InternsCalendar.objects.filter(user=request.user).exists()

    if has_calendars:
        # User has calendars, redirect to view_calendar.html
        return redirect('calendar_view')
    else:
        # User doesn't have calendars.
        messages.info(request, 'Please set up your calendar.')
        request.session['redirect_to_create_calendar'] = True
        return redirect('interns_calendar_create')

###-----------------------------------Login/end-------------------------------------###





###-----------------------------------Announcement----------------------------------###
def create_announcement(request):
    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST, request.FILES, prefix='announcement')
        recommendation_form = RecommendationForm(request.POST, request.FILES, prefix='recommendation')

        if 'all_submit' in request.POST:
            if announcement_form.is_valid() or recommendation_form.is_valid():
                announcement = announcement_form.save()
                recommendation = recommendation_form.save()
                return redirect('announcement_list')

    else:
        announcement_form = AnnouncementForm(prefix='announcement')
        recommendation_form = RecommendationForm(prefix='recommendation')

    context = {
        'announcement_form': announcement_form,
        'recommendation_form': recommendation_form,
    }

    return render(request, 'announcements/create_announcement.html', context)

def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-pub_date')
    recommendations = Recommendation.objects.all().order_by('-pub_date')

    context = {
        'announcements': announcements,
        'recommendations': recommendations,
    }

    return render(request, 'announcements/announcement_list.html', context)

def delete_item(request, item_type, item_id):
    if item_type == 'announcement':
        item = get_object_or_404(Announcement, pk=item_id)
        # Handle deletion and redirection for announcements
    elif item_type == 'recommendation':
        item = get_object_or_404(Recommendation, pk=item_id)
        # Handle deletion and redirection for recommendations
    else:
        # Handle invalid item type
        pass

    if request.method == 'POST':
        item.delete()
        return redirect('announcement_list')

    context = {
        'item': item,
        'item_type': item_type.capitalize(),  # Capitalize for display
    }

    return render(request, 'announcements/delete_item.html', context)

def delete_all_announcement(request):
    if request.method == 'POST':
        Announcement.objects.all().delete()

    return redirect('announcement_list')

def delete_all_recommendation(request):
    if request.method == 'POST':
        Recommendation.objects.all().delete()

    return redirect('announcement_list')


###-----------------------------------Announcement/end----------------------------------###


@login_required
def record_history(request):
    messages.success(request, 'Recorded history successfully.')


    return redirect('view_time_records')


def generate_time_records_text(time_records):
    text_content = "Timestamp | Action\n"

    for record in time_records:
        # Convert the timestamp to the user's timezone
        user_timezone = pytz.timezone(record.intern_user.timezone)
        timestamp_local = record.timestamp.astimezone(user_timezone)

        # Add the timestamp and action to the text content
        text_content += f"{timestamp_local} | {record.action}\n"

    return text_content

@login_required
def view_time_records(request):
    time_records = TimeRecord.objects.filter(intern_user=request.user).order_by('-timestamp')

    if 'download_history' in request.POST:
        # Generate the text content
        text_content = generate_time_records_text(time_records)

        # Create a text response and set the appropriate headers
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="time_records.txt"'
        return response

    return render(request, 'DTR/view_time_records.html', {'time_records': time_records})


def test_messages(request):
    messages.success(request, 'This is a success message.')
    messages.error(request, 'This is an error message.')
    messages.warning(request, 'This is a warning message.')
    messages.info(request, 'This is an info message.')

    return render(request, 'internship_calendar/test_messages.html')

###------------------------------------Calendar Report Page-----------------------------------------###
@login_required
def interns_calendar_create(request):
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

    if request.method == 'POST':
        form = InternsCalendarForm(request.POST)
        if form.is_valid():
            # Save the form and setup calendar
            interns_calendar = form.save(commit=False)
            interns_calendar.user = request.user  # Assuming user is authenticated
            interns_calendar.save()

            # Redirect to the calendar_view page
            return redirect('calendar_view')

    else:
        form = InternsCalendarForm()

    return render(request, 'internship_calendar/interns_calendar_create.html', {'form': form})


@login_required
def daily_accomplishment_create(request, date=None):
    user = request.user  # Assuming user is authenticated
    interns_calendar = InternsCalendar.objects.filter(user=user).last()

    # Retrieve all DailyAccomplishments for the given date (if date is provided)
    accomplishments = []
    if date:
        accomplishments = DailyAccomplishment.objects.filter(interns_calendar=interns_calendar, date=date)

    if request.method == 'POST':
        form = DailyAccomplishmentForm(request.POST, request.FILES)

        if 'rest_day' in request.POST:
            # Handle marking the day as a rest day
            daily_accomplishment = DailyAccomplishment(
                interns_calendar=interns_calendar,
                date=date,
                submitted_by=user,
                is_rest_day=True
            )
            daily_accomplishment.save()
            messages.success(request, "This day is marked as a rest day.")
            return JsonResponse({'success': True})

        else:
            # Handle regular daily accomplishment submission
            if form.is_valid():
                daily_accomplishment = form.save(commit=False)
                daily_accomplishment.interns_calendar = interns_calendar
                daily_accomplishment.date = date
                daily_accomplishment.submitted_by = user
                daily_accomplishment.save()
                messages.success(request, "Daily accomplishment report submitted.")

                accomplishment_data = {
                    'text_submission': daily_accomplishment.text_submission,
                    'hours_submission': daily_accomplishment.hours_submission,
                    'document_submission_url': daily_accomplishment.document_submission.url if daily_accomplishment.document_submission else None,
                }

                return JsonResponse({'success': True, 'accomplishment': accomplishment_data})

            else:
                # Handle form validation errors here
                return JsonResponse({'success': False})

    else:
        form = DailyAccomplishmentForm(initial={'date': date})

    return render(request, 'internship_calendar/daily_accomplishment_create.html', {
        'form': form,
        'date': date,
        'accomplishments': accomplishments,
        'bin_date': date,
    })

@login_required
def calendar_view(request):
    user = request.user  # Assuming user is authenticated
    interns_calendar = InternsCalendar.objects.filter(user=user).last()

    if interns_calendar:
        # Calculate the start date for the submission bins
        start_date = interns_calendar.start_month
        submission_bins = range(1, interns_calendar.num_submission_bins + 1)

        # Calculate the end date based on the calendar settings
        end_date = interns_calendar.end_month

        # Create a list of weeks and their submission bins
        weeks = []
        current_week_start = start_date
        current_week_number = 1
        bin_dates = []

        for bin_number in submission_bins:
            bin_date = start_date + timedelta(days=bin_number - 1)
            bin_dates.append(bin_date)

            if bin_date >= end_date:
                break

            if len(bin_dates) == 7:
                weeks.append({
                    'week_number': f'WEEK {current_week_number}',
                    'bin_dates': bin_dates,
                })
                current_week_start = bin_date + timedelta(days=1)
                bin_dates = []
                current_week_number += 1

        # If there are remaining bins, add them to the last week
        if bin_dates:
            weeks.append({
                'week_number': f'WEEK {current_week_number}',
                'bin_dates': bin_dates,
            })

        # Retrieve daily accomplishments related to this calendar
        accomplishments = DailyAccomplishment.objects.filter(interns_calendar=interns_calendar)

        # Retrieve time records for each submission bin or day
        bin_time_records = []
        for week in weeks:
            for bin_date in week['bin_dates']:
                # Retrieve time records for the current bin_date
                time_records_for_bin = TimeRecord.objects.filter(intern_user=user, timestamp__date=bin_date)
                bin_time_records.append({
                    'bin_date': bin_date,
                    'time_records': time_records_for_bin,
                })

        is_rest_day = request.GET.get('rest_day') == 'true'

        context = {
            'interns_calendar': interns_calendar,
            'accomplishments': accomplishments,
            'weeks': weeks,
            'is_rest_day': is_rest_day,
            'bin_time_records': bin_time_records,  # Include time records in the context
        }

        return render(request, 'internship_calendar/calendar_view.html', context)

    # Handle the case when there's no calendar set up
    context = {
        'message': 'No calendar set up. Please create a calendar.',
    }

    return render(request, 'internship_calendar/calendar_view.html', context)

@login_required
def calendar_detail(request, date=None):
    user = request.user  # Assuming user is authenticated

    if date is None:
        # If date is not specified, use the current date as the default
        date = date.today()

    interns_calendar = InternsCalendar.objects.filter(user=user).last()

    # Filter TimeRecord objects for the given date and interns_calendar
    time_records = TimeRecord.objects.filter(interns_calendar=interns_calendar, date=date)

    context = {
        'interns_calendar': interns_calendar,
        'time_records': time_records,
        'date': date,  # Pass the date to the template context
    }
    return render(request, 'internship_calendar/calendar_detail.html', context)


def time_in(request, date=None):
    # Retrieve the InternsCalendar associated with the user
    user = request.user  # Assuming user is authenticated
    interns_calendar = InternsCalendar.objects.filter(user=user).last()

    # Create a TimeRecord entry for Time In
    TimeRecord.objects.create(
        interns_calendar=interns_calendar,  # Associate with the retrieved calendar
        intern_user=user,
        is_time_in=True,
        action='Time In',
        date=date  # Pass the date parameter
    )
    return redirect('calendar_detail', date=date)

def time_out(request, date=None):

    user = request.user  # Assuming user is authenticated
    interns_calendar = InternsCalendar.objects.filter(user=user).last()

    # Create a TimeRecord entry for Time Out
    TimeRecord.objects.create(
        interns_calendar=interns_calendar,  # Associate with the retrieved calendar
        intern_user=user,
        is_time_in=False,
        action='Time Out',
        date=date  # Pass the date parameter
    )
    return redirect('calendar_detail', date=date)

def download_history(request):
    # Retrieve and order time records
    time_records = TimeRecord.objects.filter(intern_user=request.user).order_by('-timestamp')

    # Generate the text content
    text_content = generate_time_records_text(time_records)

    # Create a text response and set the appropriate headers for download
    response = HttpResponse(text_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="time_records.txt"'
    return response

def clear_history(request):
    if request.method == 'POST':
        TimeRecord.objects.all().delete()

    # Assuming you have a valid way to obtain the interns_calendar_id
    interns_calendar_id = 1 # Replace with the actual calendar ID
    return redirect('calendar_detail', interns_calendar_id=interns_calendar_id)

###-------------------------------------Documents----------------------------------###
@login_required
def upload_document(request):
    if request.method == 'POST':
        requirement = request.POST['requirement']
        document_image = request.FILES['document_image']
        Document.objects.create(user=request.user, requirement=requirement, document_image=document_image)
        return redirect('document_list')
    return render(request, 'documents/upload_document.html')


@login_required
def document_list(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'documents/document_list.html', {'documents': documents})

###---------------------------------Documents/end----------------------------------###


@login_required
def weekly_report(request):
    Weekly = WeeklyReport.objects.filter(user=request.user)

    if request.method == 'POST':
        Weekly_textsub = request.POST.get('Weekly_textsub')
        document_submission = request.FILES.get('document_submission')

        # Assuming you want to create a new WeeklyReport instance for the user
        # and populate the fields,

        # Create a new WeeklyReport instance for the user
        WeeklyReport.objects.create(user=request.user, Weekly_textsub=Weekly_textsub, document_submission=document_submission)

        return redirect('Weekly')

    return render(request, 'documents/Weekly.html', {'Weekly': Weekly})

