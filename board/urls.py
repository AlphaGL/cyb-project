# board/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('events/', views.events_view, name='events'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('results/', views.results_view, name='results'),
    
    # Admin Authentication
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin Announcement URLs
    path('admin/announcements/', views.admin_announcements, name='admin_announcements'),
    path('admin/announcements/add/', views.admin_add_announcement, name='admin_add_announcement'),
    path('admin/announcements/edit/<int:pk>/', views.admin_edit_announcement, name='admin_edit_announcement'),
    path('admin/announcements/delete/<int:pk>/', views.admin_delete_announcement, name='admin_delete_announcement'),
    
    # Admin Event URLs
    path('admin/events/', views.admin_events, name='admin_events'),
    path('admin/events/add/', views.admin_add_event, name='admin_add_event'),
    path('admin/events/edit/<int:pk>/', views.admin_edit_event, name='admin_edit_event'),
    path('admin/events/delete/<int:pk>/', views.admin_delete_event, name='admin_delete_event'),
    
    # Admin Timetable URLs
    path('admin/timetables/', views.admin_timetables, name='admin_timetables'),
    path('admin/timetables/add/', views.admin_add_timetable, name='admin_add_timetable'),
    path('admin/timetables/edit/<int:pk>/', views.admin_edit_timetable, name='admin_edit_timetable'),
    path('admin/timetables/delete/<int:pk>/', views.admin_delete_timetable, name='admin_delete_timetable'),
    
    # Admin Result URLs
    path('admin/results/', views.admin_results, name='admin_results'),
    path('admin/results/add/', views.admin_add_result, name='admin_add_result'),
    path('admin/results/edit/<int:pk>/', views.admin_edit_result, name='admin_edit_result'),
    path('admin/results/delete/<int:pk>/', views.admin_delete_result, name='admin_delete_result'),
    
    # Admin Department URLs
    path('admin/departments/', views.admin_departments, name='admin_departments'),
    path('admin/departments/add/', views.admin_add_department, name='admin_add_department'),
    path('admin/departments/edit/<int:pk>/', views.admin_edit_department, name='admin_edit_department'),
    path('admin/departments/delete/<int:pk>/', views.admin_delete_department, name='admin_delete_department'),
]