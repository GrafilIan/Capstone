from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .forms import AnnouncementForm, RecommendationForm
from .models import Announcement, Recommendation
from .models import intern, TimeRecord
from .forms import TimeRecordForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

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



def time_in_out(request):
    if request.method == 'POST':
        form = TimeRecordForm(request.POST)
        if form.is_valid():
            is_time_in = form.cleaned_data['is_time_in']
            TimeRecord.objects.create(is_time_in=is_time_in)
            return redirect('time_in_out')
    else:
        form = TimeRecordForm()

    time_records = TimeRecord.objects.all().order_by('-timestamp')
    return render(request, 'DTR/time_in_out.html', {'form': form, 'time_records': time_records})
