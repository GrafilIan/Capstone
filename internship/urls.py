from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('InternRegister/', views.InternRegister, name='InternRegister'),
    path('Login/', views.loginnn, name='Login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('create/', views.create_announcement, name='create_announcement'),
    path('list/', views.announcement_list, name='announcement_list'),
    path('studentlist/', views.student_announcement_list, name='student_announcement_list'),
    path('delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),
    path('view_time_records/', views.view_time_records, name='view_time_records'),
    path('delete_all_announcement/', views.delete_all_announcement, name='delete_all_announcement'),
    path('delete_all_recommendation/', views.delete_all_recommendation, name='delete_all_recommendation'),

    path('redirect-to-calendar/', views.redirect_to_calendar, name='redirect_to_calendar'),
    path('calendar-view/', views.calendar_view, name='calendar_view'),
    path('interns-calendar-create/', views.interns_calendar_create, name='interns_calendar_create'),

    path('internship/daily-accomplishment-create/<str:date>/', views.daily_accomplishment_create, name='daily_accomplishment_create'),
    path('test_messages/', views.test_messages, name='test_messages'),
    path('calendar/<str:date>/', views.calendar_detail, name='calendar_detail'),
    path('time_in/<str:date>/', views.time_in, name='time_in'),
    path('time_out/<str:date>/', views.time_out, name='time_out'),
    
    path('documents/', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('download_time_records/', views.view_time_records, name='download_time_records'),
    path('download_history/', views.download_history, name='download_history'),

    path('upload_weekly_report/', views.upload_weekly_report, name='upload_weekly_report'),
    path('weekly_report_detail/', views.weekly_report_detail, name='weekly_report_detail'),

    path('upload_narrative_report/', views.upload_narrative_report, name='upload_narrative_report'),
    path('narrative_report_detail/', views.narrative_report_detail, name='narrative_report_detail'),

    path('upload_dtr_report/', views.upload_dtr_report, name='upload_dtr_report'),
    path('dtr_detail/', views.dtr_detail, name='dtr_detail'),

#---------------------------Admin Section--------------------------#
    path('admin/interns/', views.intern_list, name='intern_list'),

]