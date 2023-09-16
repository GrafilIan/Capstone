from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import AnnouncementForm, RecommendationForm
from .models import Announcement, Recommendation
from .models import intern, TimeRecord
from .forms import TimeRecordForm
from .models import InternshipCalendar
from .forms import InternshipCalendarForm


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

def time_in_out(request):
    if request.method == 'POST':
        form = TimeRecordForm(request.POST)

        # If "Time Out" button is clicked, mark the hidden field as not required
        if 'is_time_in' in request.POST and request.POST['is_time_in'] == 'false':
            form.fields['is_time_in'].required = False

        if form.is_valid():
            is_time_in = form.cleaned_data['is_time_in']
            action = 'Time In' if is_time_in else 'Time Out'
            TimeRecord.objects.create(is_time_in=is_time_in, action=action)
            return redirect('time_in_out')
    else:
        form = TimeRecordForm()

    time_records = TimeRecord.objects.all().order_by('-timestamp')
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




