from django.urls import path
from .views import SignUpView
from . import views
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('create/', views.create_announcement, name='create_announcement'),
    path('list/', views.announcement_list, name='announcement_list'),
    path('delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),
    path('time_in_out/', views.time_in_out, name='time_in_out'),

]