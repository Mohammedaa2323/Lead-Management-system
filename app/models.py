from django.db import models

from django.utils import timezone

from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):

    role_choices=(
 
        ("salerep","salerep"),
        ("manager","manager")
    )
    role = models.CharField(max_length=200,choices=role_choices,default="salerep")
    


class Lead(models.Model):


    name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=200)
    
    status_choice = [

        ('New','New'),

        ('In progress','In progress'),

        ('Contacted','Contacted'),

        ('Qualified','Qualified'),

        ('Converted','Converted'),

        ('Closed','Closed')

    ]

    status = models.CharField(max_length=200,choices=status_choice,default="New")

    discreaption = models.TextField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    assigned_to = models.ForeignKey(User, related_name='assigned_leads', on_delete=models.SET_NULL, null=True, blank=True)

    source = models.CharField(max_length=200, default='CSV Import')

    def __str__(self):
        return self.name

class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='tasks')
    
    description = models.TextField()
    
    deadline = models.DateTimeField()

    is_compeleted = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)




class Notification(models.Model):

    NOTIFICATION_TYPE_CHOICES = [

        ('LeadAssignment', 'Lead Assignment'),

        ('StatusChange', 'Status Change'),
        
        ('TaskDeadline', 'Task Deadline'),
    
    ]
    
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    
    message = models.TextField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)