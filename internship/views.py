from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .forms import AnnouncementForm, RecommendationForm
from .models import Announcement, Recommendation
from .models import intern, TimeRecord
from .forms import TimeRecordForm
from .models import InternshipCalendar
from .forms import InternshipCalendarForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import InternsCalendar, DailyAccomplishment
from .forms import InternsCalendarForm, DailyAccomplishmentForm
from datetime import timedelta
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


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

        # If "Time Out" button is clicked, mark the hidden field as not required
        if 'is_time_in' in request.POST and request.POST['is_time_in'] == 'false':
            form.fields['is_time_in'].required = False

        if form.is_valid():
            is_time_in = form.cleaned_data['is_time_in']
            action = 'Time In' if is_time_in else 'Time Out'
            TimeRecord.objects.create(intern_user=request.user, is_time_in=is_time_in, action=action)
            return redirect('time_in_out')
    else:
        form = TimeRecordForm()

    time_records = TimeRecord.objects.filter(intern_user=request.user).order_by('-timestamp')
    return render(request, 'DTR/time_in_out.html', {'form': form, 'time_records': time_records})





def clear_history(request):
    if request.method == 'POST':
        TimeRecord.objects.all().delete()

    return redirect('time_in_out')


def create_calendar(request):
    if request.method == 'POST':
        form = InternshipCalendarForm(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.user = request.user
            calendar.save()

            # Set a session variable to indicate calendar setup is complete
            request.session['calendar_setup_complete'] = True

            # Redirect to view_calendar with a success message
            return redirect('view_calendar')
    else:
        form = InternshipCalendarForm()

    # Pass the form to the template
    return render(request, 'calendar_app/create_calendar.html', {'form': form})

def view_calendar(request):
    # Retrieve the user's calendar records
    calendars = InternshipCalendar.objects.filter(user=request.user)

    return render(request, 'calendar_app/view_calendar.html', {'calendars': calendars})

def clear_setup(request):
    if request.method == 'POST':
        InternshipCalendar.objects.all().delete()

    return redirect('view_calendar')

@login_required  # This ensures that the user is logged in
def redirect_to_calendar(request):
    # Check if the user has calendar records
    has_calendars = InternshipCalendar.objects.filter(user=request.user).exists()

    if has_calendars:
        # User has calendars, redirect to view_calendar.html
        return redirect('view_calendar')
    else:
        # User doesn't have calendars, redirect to set_up_calendar.html
        return redirect('create_calendar')


def your_login_view(request):
    error_message = None

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

                # Check if the user has calendar records
                has_calendars = InternshipCalendar.objects.filter(user=user).exists()

                print("has_calendars:", has_calendars)
                print("Number of calendar records:", InternshipCalendar.objects.filter(user=user).count())

                if has_calendars:
                    # User has calendars, redirect to view_calendar
                    return redirect('view_calendar')
                else:
                    # User doesn't have calendars, redirect to create_calendar
                    return redirect('create_calendar')
            else:
                # Authentication failed
                error_message = "Incorrect username or password."
                return render(request, 'login.html', {'error_message': error_message})

    # If GET request or login failed, render the login form
    else:
        auth_form = AuthenticationForm()

    return render(request, 'registration/login.html', {'auth_form': auth_form})

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
            daily_accomplishment = form.save(commit=False)
            daily_accomplishment.interns_calendar = interns_calendar
            daily_accomplishment.date = date
            daily_accomplishment.submitted_by = user
            daily_accomplishment.save()

            # Redirect to the calendar_view page
            return redirect('calendar_view')

    else:
        form = DailyAccomplishmentForm(initial={'date': date})

    return render(request, 'internship_calendar/daily_accomplishment_create.html', {'form': form})

def calendar_view(request):
    user = request.user  # Assuming user is authenticated
    interns_calendar = InternsCalendar.objects.filter(user=user).last()

    if interns_calendar:
        # Calculate the start date for the submission bins
        start_date = interns_calendar.start_month
        submission_bins = range(1, interns_calendar.num_submission_bins + 1)

        # Create a list of dates for the submission bins
        bin_dates = [start_date + timedelta(days=i) for i in range(interns_calendar.num_submission_bins)]

        # Adjust the submission bin numbers by subtracting 1
        adjusted_submission_bins = [bin_number - 1 for bin_number in submission_bins]

        # Combine bins with adjusted bin numbers and dates
        submission_bins_with_dates = zip(submission_bins, adjusted_submission_bins, bin_dates)

        # Retrieve daily accomplishments related to this calendar
        accomplishments = DailyAccomplishment.objects.filter(interns_calendar=interns_calendar)

        context = {
            'interns_calendar': interns_calendar,
            'accomplishments': accomplishments,
            'submission_bins_with_dates': submission_bins_with_dates,
        }

        return render(request, 'internship_calendar/calendar_view.html', context)

    # Handle the case when there's no calendar set up
    context = {
        'message': 'No calendar set up. Please create a calendar.',
    }
    return render(request, 'internship_calendar/calendar_view.html', context)
