from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.create_announcement, name='create_announcement'),
    path('list/', views.announcement_list, name='announcement_list'),
    path('delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),
    path('time_in_out/', views.time_in_out, name='time_in_out'),
    path('clear_history/', views.clear_history, name='clear_history'),
    path('delete_all_announcement/', views.delete_all_announcement, name='delete_all_announcement'),
    path('delete_all_recommendation/', views.delete_all_recommendation, name='delete_all_recommendation'),
    path('create_calendar/', views.create_calendar, name='create_calendar'),
    path('view_calendar/', views.view_calendar, name='view_calendar'),
    path('clear_setup/', views.clear_setup, name='clear_setup'),
    path('redirect-to-calendar/', views.redirect_to_calendar, name='redirect_to_calendar'),
    path('login/', views.your_login_view, name='login'),

]