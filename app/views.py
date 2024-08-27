from django.shortcuts import render,redirect

from django.views.generic import View

from app.forms import RegistartionForm,LoginForm,LeadForm,TaskForm,LeadImportForm,NotificationForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from app.models import Lead,Task,User,Notification

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

from app.decorateros import signin_required,permission_required



"""localhost:8000/signup/
method:get,post
form class RegistrationForm"""
@method_decorator([signin_required,never_cache,permission_required],name="dispatch")
class SignupView(View):


    
    def get(self,request,*args,**kwargs):
        form = RegistartionForm()

        return render(request,"login.html",{"form":form})
    
    
    def post(self,request,*args,**kwargs):
        form = RegistartionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User created sucsessfully")
            return redirect("signin")
        
        return render(request,"login.html",{"form":form})



"""localhost:8000/signin/
method:get,post
form class LoginForm"""
class SinginView(View):
    

    def get(self,request,*args,**kwargs):
        form = LoginForm()

        return render(request,"login.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user_object = authenticate(request,username = user_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")

        messages.error(request,"invalid credontion or Please Register")
        return render(request,"login.html",{"form":form})
    

"""localhost:8000/signout/
method:get"""
@method_decorator([signin_required,never_cache],name="dispatch")
class SignoutView(View):


    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    

"""localhost:8000/index/
method:get,post
"""
@method_decorator([signin_required,never_cache],name="dispatch")
class IndexView(View):


    def get(self,request,*args,**kwargs):
        return render(request,"index.html")
    

"""localhost:8000/lead/add/
method:get,post
form class Leadform"""
@method_decorator([signin_required,never_cache,permission_required],name="dispatch")
class LeadAddView(View):


    def get(self,request,*args,**kwargs):
        form=LeadForm()

        return render(request,"lead_add.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"New Lead Created sucsessfully")
            return redirect("lead_list")
        
        return render(request,"login.html",{"form":form})
    

"""localhost:8000/task/add/
method:get,post
form class TaskForm""" 
@method_decorator([signin_required,never_cache,permission_required],name="dispatch")
class TaskAddView(View):


    def get(self,request,*args,**kwargs):
        form=TaskForm()

        return render(request,"task_add.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"New Task Created sucsessfully")
            return redirect("task_list")
        
        messages.error(request,"Error in creating task")
        return render(request,"task_add.html",{"form":form})
    


"""localhost:8000/lead/list/
method:get,post"""
@method_decorator([signin_required,never_cache],name="dispatch")
class LeadListView(View):


    def get(self,request,*args,**kwargs):
        data = Lead.objects.all()

        return render(request,"lead_list.html",{"data":data})
    

"""localhost:8000/task/list/
method:get,post"""
class TaskListView(View):


    def get(self,request,*args,**kwargs):
        if not (request.user.role == "manager" or request.user.is_superuser):
            data = Task.objects.filter(user=request.user)
            return render(request,"task_list.html",{"data":data})
        else:
            data = Task.objects.all()
            return render(request,"task_list.html",{"data":data})
        

"""localhost:8000/lead/detail/
method:get,post"""
@method_decorator([signin_required,never_cache],name="dispatch")
class LeadDetailView(View):


    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        qs = Lead.objects.get(id=id)
        messages.error(request,"")

        return render(request,"lead_detail.html",{"data":qs})


"""localhost:8000/lead/update/
method:get,post"""
@method_decorator([signin_required,never_cache,permission_required],name="dispatch")
class LeadUpdateView(View):


    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        qs = Lead.objects.get(id=id)
        form = LeadForm(instance=qs)

        return render(request,"lead_update.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        qs = Lead.objects.get(id=id)
        form = LeadForm(request.POST,instance=qs)

        if form.is_valid():
            form.save()
            messages.success(request,"lead updated successfully")
            return redirect("lead_list")
        
        return render(request,"lead_update.html",{"form":form})


"""localhost:8000/lead/delete/
method:get,post"""
@method_decorator([signin_required,never_cache,permission_required],name="dispatch")
class LeadDeleteView(View):


    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        qs = Lead.objects.get(id=id).delete()
        messages.success(request,"lead deleted successfully")

        return redirect("lead_list")


"""localhost:8000/lead/add/file/
method:get,post
form class LeadImportForm"""
@method_decorator([signin_required,never_cache,permission_required],name="dispatch")
class LeadImportView(View):


    def get(self, request):
        form = LeadImportForm()

        return render(request, 'lead_file.html', {'form': form})

    def post(self, request):
        form = LeadImportForm(request.POST, request.FILES)
        if form.is_valid():
            form.import_leads()
            messages.success(request,"lead Created successfully")
            return redirect("lead_list")

        return render(request,"lead_file.html",{"form":form})


"""localhost:8000/norification
method:get,post"""
@method_decorator([signin_required,never_cache,permission_required],name="dispatch")
class NotificationAddView(View):


    def get(self,request,*args,**kwargs):
        form = NotificationForm()

        return render(request,"notification.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"New noticication add sucsessfully")
            return redirect("index")
        
        messages.error(request,"Error in creating Notification")
        return render(request,"notification.html",{"form":form})
    


"""localhost:8000/notification/list/
method:get,post"""
class NotificationListView(View):


    def get(self,request,*args,**kwargs):
        if not (request.user.role == "manager" or request.user.is_superuser):
            data = Notification.objects.filter(user=request.user)
        else:
            data = Notification.objects.all()
            return render(request,"notification_list.html",{"data":data})

        return render(request,"notification_list.html",{"data":data})


def summary_page(request):
    total_leads = Lead.objects.count()
    total_tasks = Task.objects.count()
    
    context = {
        'total_leads': total_leads,
        'total_tasks': total_tasks,
    }
    
    return render(request, 'summary_page.html', context)