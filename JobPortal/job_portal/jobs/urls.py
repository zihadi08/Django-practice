from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.redirect_view, name='redirect_view'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Employer URLs
    path('employer/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/post/', views.post_job, name='post_job'),
    path('employer/job/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('employer/job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('employer/job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('employer/jobs/previous/', views.previous_jobs, name='previous_jobs'),
    path('employer/applicants/', views.view_all_applicants, name='view_all_applicants'),
    path('employer/jobs/search/', views.employer_dashboard, name='employer_job_search'),
    path('employer/application/<int:application_id>/status/', views.change_status, name='status'),

    # # Applicant URLs
    path('applicant/', views.applicant_dashboard, name='applicant_dashboard'),
    path('applicant/job/<int:job_id>/apply/', views.apply_for_job, name="apply_for_job"),
    path('applicant/jobs/search/', views.applicant_dashboard, name='applicant_job_search'),
    path('applicant/applications/', views.my_applications, name='my_applications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)