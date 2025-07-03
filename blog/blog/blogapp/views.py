from django.shortcuts import render

# Create your views here.

from .models import Post, Category
from django.contrib.auth.decorators import login_required
from blogapp.common_function import checkUserPermission

@login_required
def home(request):
    if not checkUserPermission(request, "can_view", "/blog/"):
        return render(request, "blogapp/403.html")
    
    blogs = Post.objects.filter(status='published')
    return render(request, 'blogapp/home.html', {'blogs': blogs})

