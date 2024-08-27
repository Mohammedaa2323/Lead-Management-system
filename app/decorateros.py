from django.shortcuts import redirect

from django.contrib import messages

from app.models import User

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"signin required")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


def permission_required(fn):
    def wrapper(request,*args,**kwargs):
        if not (request.user.role == 'manager' or request.user.is_superuser):
            messages.error(request,"only manager or admin can perform this task task")
            return redirect("index")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


