from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from main_app.forms import JobPostForm, LoginForm, RegisterForm
from main_app.models import Category, JobPost, Jobseeker_Profile, Recruiter_Profile, Skill
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
        # myuser = request.user
        # if myuser.user_type == 'Recruiter':
        #     profile_data = get_object_or_404(Recruiter_Profile, myuser=myuser)
        #     template_name = 'recruiter/profile.html'
        # elif myuser.user_type == 'JobSeeker':
        #     profile_data = get_object_or_404(Jobseeker_Profile, myuser=myuser)
        #     template_name = 'jobseeker/profile.html'
        # else:
        #     # Handle other user types or provide a default template
        #     profile_data = None
            

        # return render(request, template_name, {'profile_data': profile_data})


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
   
    user = request.user
    if user.is_authenticated:
        if user.user_type == "Recruiter":
         
            if request.method == "POST":
                form = JobPostForm(request.POST)
                if form.is_valid():
                    jobpost = form.save(commit=False)

                    # Use get_or_create to get the Recruiter_Profile or create it if it doesn't exist
                    recruiter_profile, created = Recruiter_Profile.objects.get_or_create(user_profile=user)

                    jobpost.recruiter = recruiter_profile
                    jobpost.save()

                    skill_id = request.POST.getlist('skill_set')
                    selected_skills = Skill.objects.filter(id__in=skill_id)

                    jobpost.skill_set.set(selected_skills)
                    return redirect("joblist")
            else:
                form = JobPostForm()
            return render(request, 'recruiter/create_job.html', {'form': form})
        else:
            return HttpResponseForbidden("You do not have permission to create a job post.")
    else:
        return HttpResponseForbidden("You need to be logged in to create a job post.")

@login_required
def job_list(request):
    categories = Category.objects.all()
    title_filter = request.GET.get('title', '')
    category_filter = request.GET.get('category', '')
    jobs = JobPost.objects.filter(title__icontains=title_filter)
    if category_filter:
        jobs = jobs.filter(category__id=category_filter)

    # Check if the user is a JobSeeker and has a JobSeekerProfile
    if request.user.is_authenticated and request.user.user_type == 'JobSeeker':
        try:
            job_seeker_profile = Jobseeker_Profile.objects.get(user_profile=request.user)
        except Jobseeker_Profile.DoesNotExist:
            # If the JobSeekerProfile does not exist, create one
            job_seeker_profile = Jobseeker_Profile.objects.create(user_profile=request.user)
            # You can redirect to a profile creation page or do something else if needed

        # Extract job seeker's skills
        job_seeker_skills = job_seeker_profile.skills.all()
        # Find jobs that require at least one of the job seeker's skills
        matching_jobs = JobPost.objects.filter(skill_set__in=job_seeker_skills).distinct()
    else:
        job_seeker_profile = None
        matching_jobs = None

    return render(request, 'recruiter/job_list.html', {'jobs': jobs, 'matching_jobs': matching_jobs, 'categories': categories, 'title_filter': title_filter, 'category_filter': category_filter})