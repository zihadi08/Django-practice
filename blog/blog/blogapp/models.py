from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField 
from django.contrib.auth.models import User

class MenuList(models.Model):
    module_name        = models.CharField(max_length=100, db_index=True)
    menu_name          = models.CharField(max_length=100, unique=True, db_index=True)
    menu_url           = models.CharField(max_length=250, unique=True)
    menu_icon          = models.CharField(max_length=250, blank=True, null=True)
    parent_id          = models.IntegerField()
    is_main_menu       = models.BooleanField(default=False)
    is_sub_menu        = models.BooleanField(default=False)
    is_sub_child_menu  = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(blank=True, null=True)
    deleted_at         = models.DateTimeField(blank=True, null=True)
    created_by         = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active          = models.BooleanField(default=True)
    deleted            = models.BooleanField(default=False)

    class Meta:
        db_table = "menu_list"

    def __str__(self) -> str:
        return self.menu_name

class UserPermission(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_user_for_permission") 
    menu          = models.ForeignKey(MenuList, on_delete=models.CASCADE, related_name="menu_for_permission") 
    can_view      = models.BooleanField(default=False)
    can_add       = models.BooleanField(default=False)
    can_update    = models.BooleanField(default=False)
    can_delete    = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by_user") 
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_by_user", blank=True, null=True) 
    deleted_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deleted_by_user", blank=True, null=True)
    is_active     = models.BooleanField(default=True)
    deleted       = models.BooleanField(default=False)

    class Meta:
        db_table = "user_permission"

    def __str__(self):
        return str(self.menu)




# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    slug= models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1 
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug=models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    Category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    description= RichTextField(blank=True, null=True)  
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug= base_slug
            counter = 1 
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    