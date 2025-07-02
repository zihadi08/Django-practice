from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Profile
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def task_list(request):
    task = Task.objects.order_by('-created_at')
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
            return redirect('task:list')
        
    return render(request, 'task/task_list.html', {'task':task})

@require_POST
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task:list')

@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task:list')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['date_of_birth']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'task/register.html', {'error': 'Username already taken'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, phone=phone, date_of_birth=dob)

        return redirect('task:login')
    return render(request, 'task/register.html')

def login_view(request):
    if request.method == "POST":
        phone = request.POST['phone']
        password = request.POST['password']

        try:
            profile = Profile.objects.get(phone=phone)
            user = authenticate(request, username=profile.user.username, password=password)
            if user:
                login(request, user)
                return redirect('task:list')
            else:
                return render(request, 'task/login.html', {'error': 'invalid credentials'})
        except Profile.DoesNotExist:
            return render(request, 'task/login.html', {'error': 'User not found'})
    
    return render(request, 'task/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('task:login')

@login_required
def change_password(request):
    if request.method == "POST":
        current = request.POST['current_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if not request.user.check_password(current):
            return render(request, 'task/change_password.html', {'error':'Password incorrect'})
        if new != confirm:
            return render(request, 'task/change_password.html', {'error':'New passwords do not match'})
        
        request.user.set_password(new)
        request.user.save()
        #to keep the user logged in after changing their password
        #update_session_auth_hash(request, request.user) #Prevent logout
        return redirect('task:list')

    return render(request, 'task/change_password.html')