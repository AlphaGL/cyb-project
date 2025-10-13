# board/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Announcement, Event, Timetable, Result, Department
from .forms import AdminLoginForm, AnnouncementForm, EventForm, TimetableForm, ResultForm, DepartmentForm


def ping_view(request):
    return JsonResponse({"status": "OK"})

# Public Views
def home(request):
    """Homepage with latest announcements and events"""
    # Get search query if any
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    # Get all departments for filter
    departments = Department.objects.all()
    
    # Filter announcements
    announcements = Announcement.objects.filter(is_active=True)
    if search_query:
        announcements = announcements.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    if department_filter:
        announcements = announcements.filter(department_id=department_filter)
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(
        is_active=True,
        start_date__gte=timezone.now()
    )[:5]
    
    # Get recent announcements (limit to 10)
    recent_announcements = announcements[:10]
    
    context = {
        'announcements': recent_announcements,
        'upcoming_events': upcoming_events,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter
    }
    return render(request, 'board/home.html', context)

def announcements_view(request):
    """All announcements page with pagination"""
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    departments = Department.objects.all()
    announcements = Announcement.objects.filter(is_active=True)
    
    if search_query:
        announcements = announcements.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    if department_filter:
        announcements = announcements.filter(department_id=department_filter)
    
    paginator = Paginator(announcements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter
    }
    return render(request, 'board/announcements.html', context)

def events_view(request):
    """All events page"""
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    departments = Department.objects.all()
    events = Event.objects.filter(is_active=True)
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    if department_filter:
        events = events.filter(department_id=department_filter)
    
    context = {
        'events': events,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter
    }
    return render(request, 'board/events.html', context)

def timetable_view(request):
    """Timetable view"""
    department_filter = request.GET.get('department', '')
    level_filter = request.GET.get('level', '')
    
    departments = Department.objects.all()
    timetables = Timetable.objects.filter(is_active=True)
    
    if department_filter:
        timetables = timetables.filter(department_id=department_filter)
    if level_filter:
        timetables = timetables.filter(level=level_filter)
    
    # Group by day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    timetable_by_day = {}
    for day in days:
        timetable_by_day[day] = timetables.filter(day_of_week=day)
    
    # Get unique levels for filter
    levels = Timetable.objects.values_list('level', flat=True).distinct()
    
    context = {
        'timetable_by_day': timetable_by_day,
        'departments': departments,
        'levels': levels,
        'department_filter': department_filter,
        'level_filter': level_filter
    }
    return render(request, 'board/timetable.html', context)

def results_view(request):
    """Results view"""
    department_filter = request.GET.get('department', '')
    session_filter = request.GET.get('session', '')
    
    departments = Department.objects.all()
    results = Result.objects.filter(is_published=True)
    
    if department_filter:
        results = results.filter(department_id=department_filter)
    if session_filter:
        results = results.filter(session=session_filter)
    
    # Get unique sessions for filter
    sessions = Result.objects.values_list('session', flat=True).distinct()
    
    context = {
        'results': results,
        'departments': departments,
        'sessions': sessions,
        'department_filter': department_filter,
        'session_filter': session_filter
    }
    return render(request, 'board/results.html', context)

# Admin Views
def admin_login(request):
    """Custom admin login"""
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'board/admin/login.html', {'form': form})

@login_required
def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get statistics
    total_announcements = Announcement.objects.count()
    active_announcements = Announcement.objects.filter(is_active=True).count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).count()
    
    context = {
        'total_announcements': total_announcements,
        'active_announcements': active_announcements,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'board/admin/dashboard.html', context)

# Announcement CRUD
@login_required
def admin_announcements(request):
    """List all announcements in admin"""
    if not request.user.is_staff:
        return redirect('home')
    
    announcements = Announcement.objects.all()
    return render(request, 'board/admin/announcements/list.html', {'announcements': announcements})

@login_required
def admin_add_announcement(request):
    """Add new announcement"""
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('admin_announcements')
    else:
        form = AnnouncementForm()
    
    return render(request, 'board/admin/announcements/form.html', {'form': form, 'title': 'Add Announcement'})

@login_required
def admin_edit_announcement(request, pk):
    """Edit announcement"""
    if not request.user.is_staff:
        return redirect('home')
    
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated successfully!')
            return redirect('admin_announcements')
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'board/admin/announcements/form.html', {'form': form, 'title': 'Edit Announcement'})

@login_required
def admin_delete_announcement(request, pk):
    """Delete announcement"""
    if not request.user.is_staff:
        return redirect('home')
    
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully!')
        return redirect('admin_announcements')
    
    return render(request, 'board/admin/announcements/delete.html', {'announcement': announcement})

# Similar CRUD views for Events, Timetables, Results
@login_required
def admin_events(request):
    if not request.user.is_staff:
        return redirect('home')
    events = Event.objects.all()
    return render(request, 'board/admin/events/list.html', {'events': events})

@login_required
def admin_add_event(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('admin_events')
    else:
        form = EventForm()
    
    return render(request, 'board/admin/events/form.html', {'form': form, 'title': 'Add Event'})

@login_required
def admin_edit_event(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('admin_events')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'board/admin/events/form.html', {'form': form, 'title': 'Edit Event'})

@login_required
def admin_delete_event(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('admin_events')
    
    return render(request, 'board/admin/events/delete.html', {'event': event})

# Timetable CRUD
@login_required
def admin_timetables(request):
    if not request.user.is_staff:
        return redirect('home')
    timetables = Timetable.objects.all()
    return render(request, 'board/admin/timetables/list.html', {'timetables': timetables})

@login_required
def admin_add_timetable(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.created_by = request.user
            timetable.save()
            messages.success(request, 'Timetable entry created successfully!')
            return redirect('admin_timetables')
    else:
        form = TimetableForm()
    
    return render(request, 'board/admin/timetables/form.html', {'form': form, 'title': 'Add Timetable Entry'})

@login_required
def admin_edit_timetable(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    timetable = get_object_or_404(Timetable, pk=pk)
    
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry updated successfully!')
            return redirect('admin_timetables')
    else:
        form = TimetableForm(instance=timetable)
    
    return render(request, 'board/admin/timetables/form.html', {'form': form, 'title': 'Edit Timetable Entry'})

@login_required
def admin_delete_timetable(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        messages.success(request, 'Timetable entry deleted successfully!')
        return redirect('admin_timetables')
    
    return render(request, 'board/admin/timetables/delete.html', {'timetable': timetable})

# Result CRUD
@login_required
def admin_results(request):
    if not request.user.is_staff:
        return redirect('home')
    results = Result.objects.all()
    return render(request, 'board/admin/results/list.html', {'results': results})

@login_required
def admin_add_result(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.save()
            messages.success(request, 'Result created successfully!')
            return redirect('admin_results')
    else:
        form = ResultForm()
    
    return render(request, 'board/admin/results/form.html', {'form': form, 'title': 'Add Result'})

@login_required
def admin_edit_result(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    result = get_object_or_404(Result, pk=pk)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result updated successfully!')
            return redirect('admin_results')
    else:
        form = ResultForm(instance=result)
    
    return render(request, 'board/admin/results/form.html', {'form': form, 'title': 'Edit Result'})

@login_required
def admin_delete_result(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    result = get_object_or_404(Result, pk=pk)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Result deleted successfully!')
        return redirect('admin_results')
    
    return render(request, 'board/admin/results/delete.html', {'result': result})

# Department CRUD
@login_required
def admin_departments(request):
    if not request.user.is_staff:
        return redirect('home')
    departments = Department.objects.all()
    return render(request, 'board/admin/departments/list.html', {'departments': departments})

@login_required
def admin_add_department(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('admin_departments')
    else:
        form = DepartmentForm()
    
    return render(request, 'board/admin/departments/form.html', {'form': form, 'title': 'Add Department'})

@login_required
def admin_edit_department(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('admin_departments')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'board/admin/departments/form.html', {'form': form, 'title': 'Edit Department'})

@login_required
def admin_delete_department(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('admin_departments')
    
    return render(request, 'board/admin/departments/delete.html', {'department': department})