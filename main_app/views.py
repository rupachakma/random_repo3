from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from main_app.forms import JobPostForm, LoginForm, RegisterForm
from main_app.models import JobPost, Jobseeker_Profile, Recruiter_Profile, Skill
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loginpage")
    else:
        form = RegisterForm()
    return render(request,"register.html",{'form':form})

def loginpage(request):

    if request.method == "POST":
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                user_type = user.user_type
                if user_type == 'Recruiter':
                    return redirect("profile_page")
                elif user_type == 'Jobseeker':
                    return redirect("profile_page")
                else:
                    return HttpResponse("Invalid Request")
    else:
        form = LoginForm()
    return render(request,"login.html",{'form':form})

@login_required
def profile_page(request):
        user = request.user
        if user.is_authenticated:
            # print(f"User Type: {request.user.user_type}")
            if user.user_type == 'Recruiter':
                templates_name = "recruiter/profile.html"

            elif user.user_type == 'Jobseeker':
                templates_name = "jobseeker/profile.html"
            else:
                return HttpResponse("Invalid User")
        else:
            return HttpResponse("User is not Authenticated")

        return render(request,templates_name)

def logout_page(request):
    logout(request)
    return redirect("loginpage")

@login_required
def create_jobpost(request):
    # user = request.user
    # if user.is_authenticated:
    #     if user.user_type == "Recruiter":
            if request.method == "POST":
                form = JobPostForm(request.POST)
                if form.is_valid():
                    jobpost = form.save(commit=False)

                    jobpost.Recruiter = request.user
                    jobpost.save()

                    skill_id = request.POST.getlist('skill_set')
                    selected_skills = Skill.objects.filter(id__in=skill_id)

                    jobpost.skill_set.set(selected_skills)
                    return redirect('jobs')
            else:
                form = JobPostForm()
            return render(request, 'recruiter/create_job.html', {'form': form})
    #     else:
    #         return HttpResponseForbidden("You do not have permission to create a job post.")
    # else:
    #     return HttpResponseForbidden("You need to be logged in to create a job post.")
    
