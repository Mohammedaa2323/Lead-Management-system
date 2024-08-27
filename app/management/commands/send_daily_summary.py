from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from app.models import Lead, Task ,User

User = get_user_model()

class Command(BaseCommand):
    help = 'Send daily summary emails to users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        today = timezone.now().date()

        for user in users:
            leads = Lead.objects.filter(assigned_to=user, created_date__date=today)
            tasks = Task.objects.filter(user=user,is_compeleted=False)

            if leads.exists() or tasks.exists():
                subject = f"Daily Summary for {today}"
                message = self.generate_summary(user, leads, tasks)
                send_mail(
                    subject,
                    message,
                    'manager@example.com',
                    [user.email],
                    fail_silently=False,
                )

    def generate_summary(self, user, leads, tasks):
        summary = f"Hello {user.username},\n\nHere is your daily summary for today:\n\n"

        if leads.exists():
            summary += "New Leads Assigned:\n"
            for lead in leads:
                summary += f"- {lead.name} (Contact: {lead.phone})\n"
                summary += f"- status : {lead.status}\n"

        if tasks.exists():
            summary += "\nPending Tasks:\n"
            for task in tasks:
                summary += f"- {task.title} (Deadline: {task.deadline})\n"

        summary += "\nBest Regards,\nYour Lead Management Team"
        return summary