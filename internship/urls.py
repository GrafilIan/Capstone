from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('InternRegister/', views.InternRegister, name='InternRegister'),
    path('Login/', views.loginnn, name='Login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.create_announcement, name='create_announcement'),
    path('list/', views.announcement_list, name='announcement_list'),
    path('delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),
    path('view_time_records/', views.view_time_records, name='view_time_records'),
    path('clear_history/', views.clear_history, name='clear_history'),
    path('delete_all_announcement/', views.delete_all_announcement, name='delete_all_announcement'),
    path('delete_all_recommendation/', views.delete_all_recommendation, name='delete_all_recommendation'),
    path('redirect-to-calendar/', views.redirect_to_calendar, name='redirect_to_calendar'),
    path('interns-calendar-create/', views.interns_calendar_create, name='interns_calendar_create'),
    path('internship/daily-accomplishment-create/<str:date>/', views.daily_accomplishment_create, name='daily_accomplishment_create'),
    path('calendar-view/', views.calendar_view, name='calendar_view'),
    path('test_messages/', views.test_messages, name='test_messages'),
    path('documents/', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('download_time_records/', views.view_time_records, name='download_time_records'),
    path('download_history/', views.download_history, name='download_history'),
    path('', views.my_view, name='StudentCalendar'),

    path('calendar/<int:interns_calendar_id>/', views.calendar_detail, name='calendar_detail'),
    path('time_in/<int:interns_calendar_id>/', views.time_in, name='time_in'),
    path('time_out/<int:interns_calendar_id>/', views.time_out, name='time_out'),
]