from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import AnnouncementForm, RecommendationForm
from .models import Announcement, Recommendation
from .models import intern, TimeRecord
from .forms import TimeRecordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import InternsCalendar, DailyAccomplishment
from .forms import InternsCalendarForm, DailyAccomplishmentForm
from .models import Document
from datetime import timedelta
from django.utils.timezone import now
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


@login_required
def time_in_out(request):
    if request.method == 'POST':
        form = TimeRecordForm(request.POST)

        if 'is_time_in' in request.POST and request.POST['is_time_in'] == 'false':
            form.fields['is_time_in'].required = False

        if form.is_valid():
            is_time_in = form.cleaned_data['is_time_in']
            action = 'Time In' if is_time_in else 'Time Out'
            TimeRecord.objects.create(intern_user=request.user, is_time_in=is_time_in, action=action)

            # Set a success message
            messages.success(request, 'Time Record saved successfully.')

            if 'record_history' in request.POST:
                # Redirect to the page where you can view the saved history
                return redirect('view_time_records')

    else:
        form = TimeRecordForm()

    time_records = TimeRecord.objects.filter(intern_user=request.user).order_by('-timestamp')
    return render(request, 'DTR/time_in_out.html', {'form': form, 'time_records': time_records})


@login_required
def view_time_records(request):
    time_records = TimeRecord.objects.filter(intern_user=request.user).order_by('-timestamp')

    return render(request, 'DTR/view_time_records.html', {'time_records': time_records})


def clear_history(request):
    if request.method == 'POST':
        TimeRecord.objects.all().delete()

    return redirect('time_in_out')



@login_required  # This ensures that the user is logged in
def redirect_to_calendar(request):
    # Check if the user has calendar records
    has_calendars = InternsCalendarForm.objects.filter(user=request.user).exists()

    if has_calendars:
        # User has calendars, redirect to view_calendar.html
        return redirect('calendar_view')
    else:
        # User doesn't have calendars, redirect to set_up_calendar.html
        messages.info(request, 'Please set up your calendar.')
        request.session['redirect_to_create_calendar'] = True
        return redirect('interns_calendar_create')





def interns_calendar_create(request):
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


def daily_accomplishment_create(request, date=None):
    user = request.user  # Assuming user is authenticated
    interns_calendar = InternsCalendar.objects.filter(user=user).last()

    if request.method == 'POST':
        form = DailyAccomplishmentForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the "Rest Day" button is clicked
            if 'rest_day' in request.POST:
                # Handle the rest day logic here
                # Create a new DailyAccomplishment instance and set is_rest_day to True
                daily_accomplishment = DailyAccomplishment(
                    interns_calendar=interns_calendar,
                    date=date,
                    submitted_by=user,
                    is_rest_day=True  # Set the rest day flag
                )
                daily_accomplishment.save()
                messages.success(request, "This day is marked as a rest day.")
            else:
                daily_accomplishment = form.save(commit=False)
                daily_accomplishment.interns_calendar = interns_calendar
                daily_accomplishment.date = date
                daily_accomplishment.submitted_by = user
                daily_accomplishment.save()
                messages.success(request, "Daily accomplishment report submitted.")

            # Redirect to the calendar_view page
            return redirect('calendar_view')

    else:
        form = DailyAccomplishmentForm(initial={'date': date})

    return render(request, 'internship_calendar/daily_accomplishment_create.html', {'form': form, 'date': date})

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

        context = {
            'interns_calendar': interns_calendar,
            'accomplishments': accomplishments,
            'weeks': weeks,
        }

        return render(request, 'internship_calendar/calendar_view.html', context)

    # Handle the case when there's no calendar set up
    context = {
        'message': 'No calendar set up. Please create a calendar.',
    }
    return render(request, 'internship_calendar/calendar_view.html', context)

def test_messages(request):
    messages.success(request, 'This is a success message.')
    messages.error(request, 'This is an error message.')
    messages.warning(request, 'This is a warning message.')
    messages.info(request, 'This is an info message.')

    return render(request, 'internship_calendar/test_messages.html')

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

