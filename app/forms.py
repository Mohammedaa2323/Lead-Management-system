from django import forms

from django.contrib.auth.forms import UserCreationForm

from app.models import User,Lead,Task,Notification

import csv



class RegistartionForm(UserCreationForm):


    class Meta:

        model = User

        fields = ["username","email","password1","password2","role"]


class LoginForm(forms.Form):


    username = forms.CharField()

    password = forms.CharField()


class LeadForm(forms.ModelForm):

        def __init__(self,*args,**kwargs):
            super (LeadForm,self ).__init__(*args,**kwargs) # populates the post
            self.fields['assigned_to'].queryset = User.objects.filter(role='salerep')

        class Meta:
            
            model = Lead
    
            fields = ["name","email","phone","status","discreaption","assigned_to"]

            widgets={

            "name":forms.TextInput(attrs={"class":"form-control"}),

            "email":forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'class': 'form-control'}),

            "assigned_to":forms.Select(attrs={"class":"form-control from-select"}),

            "discreaption":forms.TextInput(attrs={"class":"form-control"}),

            "phone":forms.NumberInput(attrs={"class":"form-control"}),

            "status":forms.Select(attrs={"class":"form-control from-select"}),


        }
    

class TaskForm(forms.ModelForm):
     def __init__(self,*args,**kwargs):
        super (TaskForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['user'].queryset = User.objects.filter(role='salerep')

     
     class Meta:
          
          model = Task

          fields = ["user","title","lead","description","deadline","is_compeleted"]

          widgets={
               
            "user":forms.Select(attrs={"class":"form-control from-select"}),

            "title":forms.TextInput(attrs={"class":"form-control"}),

            "lead":forms.Select(attrs={"class":"form-control from-select"}),

            "description":forms.TextInput(attrs={"class":"form-control"}),

            "deadline":forms.DateInput(attrs={"class":"form-control",'type': 'date'}),

            # "is_compeleted":forms.CheckboxInput(attrs={"class":"form-control"}),


         }
          
    
class LeadImportForm(forms.Form):
    csv_file = forms.FileField()

    def import_leads(self):
        csv_file = self.cleaned_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        # print(decoded_file)
        reader = csv.DictReader(decoded_file)  
        print(reader)
        for row in reader:
            print(row)
            Lead.objects.create(
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                # status=row['status'],
                discreaption=row['discreaption'],
                status=row.get('status', 'New'),
                source=row.get('source', 'CSV Import'),
                assigned_to=User.objects.get(username=row['assigned_to'])
                )


class NotificationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (NotificationForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['user'].queryset = User.objects.filter(role='salerep')

     

    class Meta:

        model = Notification

        fields = ["type","message","user","lead","is_read"]


        widgets={
               
            "user":forms.Select(attrs={"class":"form-control from-select"}),

            "type":forms.Select(attrs={"class":"form-control from-select"}),

            "lead":forms.Select(attrs={"class":"form-control from-select"}),

            "message":forms.TextInput(attrs={"class":"form-control"}),

         }