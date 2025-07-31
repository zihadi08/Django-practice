from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RegistrationForm, PostJobForm, ApplicationForm
from .models import Profile, Job, Application

# Create your views here.

@login_required
def redirect_view(request):
    profile = request.user.profile
    if profile.role == 'employer':
        return redirect('employer_dashboard')
    else:
        return redirect('applicant_dashboard')
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = form.cleaned_data['role']
            user.profile.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('redirect_view')
    else:
        form = RegistrationForm()
    return render(request, 'jobs/register.html', {'form': form})


# Employer features
@login_required
def employer_dashboard(request):
    searched_jobs = Job.objects.none()  # Initialize with an empty queryset
    jobs = Job.objects.filter(posted_by=request.user.profile, is_active=True)
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            searched_jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(company_name__icontains=query) |
                Q(location__icontains=query)
            )
        print(request.user.profile.role)
    return render(request, 'jobs/employer_dashboard.html', {'searched_job': searched_jobs, 'jobs':jobs, 'query': query, 'profile': request.user.profile})

# @login_required
# def edit_job(request, job_id):
#     job = Job.objects.get(id=job_id, posted_by=request.user.profile)
#     if request.method == 'POST':
#         form = PostJobForm(request.POST, instance=job)
#         if form.is_valid():
#             form.save()
#             return redirect('employer_dashboard')
#     else:
#         form = PostJobForm(instance=job)
#     return render(request, 'jobs/edit_job.html', {'form': form, 'job': job, 'profile': request.user.profile})

# @login_required
# def delete_job(request, job_id):
#     job = Job.objects.get(id=job_id, posted_by=request.user.profile, is_active=True)
#     if request.method == 'POST':
#         if job.is_active:
#             job.is_active = False
#         job.save()
#         return redirect('employer_dashboard')
#     return render(request, 'jobs/delete_job.html', {'job': job, 'profile': request.user.profile})

# @login_required
# def previous_jobs(request):
#     jobs = Job.objects.filter(posted_by=request.user.profile, is_active=False)
#     return render(request, 'jobs/previous_jobs.html', {'jobs': jobs, 'profile': request.user.profile})

@login_required
def view_applicants(request, job_id):
    job = Job.objects.get(id=job_id, posted_by=request.user.profile, is_active=True)
    applications = Application.objects.filter(job=job)
    return render(request, 'jobs/view_applicants.html', {'job': job, 'applications': applications, 'profile': request.user.profile})

# @login_required
# def view_all_applicants(request):
#     jobs = Job.objects.filter(posted_by=request.user.profile)
#     applications = Application.objects.filter(job__in=jobs)
#     return render(request, 'jobs/view_all_applicants.html', {'jobs': jobs, 'applications': applications, 'profile': request.user.profile})

@login_required
def post_job(request):
    form = PostJobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.posted_by = request.user.profile
        job.save()
        return redirect('employer_dashboard')
    return render(request, 'jobs/post_job.html', {'form': form, 'profile': request.user.profile})

@login_required
def change_status(request, application_id):
    application = Application.objects.get(id=application_id, job__posted_by=request.user.profile)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Application.STATUS_CHOICES):
            if application.status == 'Under Review':
                application.status = status
                application.save()
                messages.success(request, f"Application status changed to {status}.")
                return redirect('view_applicants', job_id=application.job.id)
            else:
                messages.warning(request, f"Application already {application.status}. You can only change the status of applications that are under review.")
                return redirect('view_applicants', job_id=application.job.id)
        else:
            messages.error(request, "Invalid status.")
            return redirect('view_applicants', job_id=application.job.id)
    return render(request, 'jobs/change_status.html', {'application': application, 'profile': request.user.profile})









# Applicant features
@login_required
def applicant_dashboard(request):
    searched_jobs = Job.objects.none()  # Initialize with an empty queryset
    jobs = Job.objects.filter(is_active=True)
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            searched_jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(company_name__icontains=query) |
                Q(location__icontains=query)
            )
    return render(request, 'jobs/applicant_dashboard.html', {'searched_job': searched_jobs, 'jobs':jobs, 'query': query, 'profile': request.user.profile})

@login_required
def apply_for_job(request, job_id):
    job = Job.objects.get(id=job_id)
    application = Application.objects.filter(applicant=request.user.profile, job=job)
    if not application.exists():
        if request.method == 'POST':
        
            form = ApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.job = job
                application.applicant = request.user.profile
                application.save()
                messages.success(request, "You have successfully applied for the job.")
                return redirect('applicant_dashboard')
        else:
            form = ApplicationForm()
    else:
        messages.warning(request, "You have already applied for this job.")
        return redirect('my_applications')  # or the job detail page
    return render(request, 'jobs/apply_job.html', {'job': job, 'form': form, 'profile': request.user.profile})

@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user.profile)
    return render(request, 'jobs/my_applications.html', {'applications': applications, 'msg': messages.warning, 'profile': request.user.profile})

# @login_required
# def applicant_dashboard(request):
#     status_filter = request.GET.get('status')
#     applications = request.user.profile.applications.all()
#     if status_filter:
#         applications = applications.filter(status=status_filter)
#     return render(request, 'jobs/applicant_dashboard.html', {
#         'applications': applications,
#         'status_filter': status_filter
#     })

# need more time to fix this; Sorry :)