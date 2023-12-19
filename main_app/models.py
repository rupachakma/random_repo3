from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill,blank=True)
    def __str__(self):
        return self.display_name

class Recruiter_Profile(models.Model):
    user_profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="image",blank=True,null=True)
    company_name = models.CharField(max_length = 100)
    address = models.TextField()
    def __str__(self):
        return self.user_profile.username
    
class Jobseeker_Profile(models.Model):
    user_profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="image",blank=True,null=True)
    skills = models.ManyToManyField(Skill)
    resume = models.FileField(upload_to='resumes/')
    def __str__(self):
        return self.user_profile.username
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class JobPost(models.Model):
    recruiter = models.ForeignKey(Recruiter_Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    openings = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    skill_set = models.ManyToManyField(Skill)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title