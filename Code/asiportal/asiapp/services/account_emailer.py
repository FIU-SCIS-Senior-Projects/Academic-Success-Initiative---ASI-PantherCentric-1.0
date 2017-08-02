from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.template.loader import get_template
from courses.models import Course
from django.conf import settings

def send_account_confirmation_link(user, tok):
    title = '[ASI] Account Activation Link'
    email_template = get_template('account_confirmation.html')
    email_context = {
                        'user' : user,
                        'link' : tok.get_absolute_url(),
                     }
    message = email_template.render(email_context)
    email = EmailMessage(
            title,
            message,
            'asi-noreply@cs.fiu.edu',
            [user.email],
            bcc=['asisoftwaretest@gmail.com']
            )
    email.content_subtype = 'html'
    email.send()

def send_email_alert(user):
    title = '[ASI] New Semester, New Site!'
    dangle = ['a', 'b']
    courses = Course.objects.all()
    email_template = get_template('mass_email.html')
    email_context = {
                        'user' : user,
                        'courses' : courses,
                        'something_else' : courses.count(),
                     }
    message = email_template.render(email_context)
    email = EmailMessage(
            title,
            message,
            'asi-noreply@cs.fiu.edu',
            [user.email],
            bcc=['asisoftwaretest@gmail.com']
            )
    email.content_subtype = 'html'
    email.send()

def send_reminder(user, sessions, date):
    title = "[ASI] Reminder for Today's Session(s)"
    email_template = get_template('reminder.html')
    email_context = {
                        'user' : user,
                        'sessions' : sessions,
                        'date': date
                     }
    message = email_template.render(email_context)
    email = EmailMessage(
            title,
            message,
            settings.EMAIL_HOST_USER,
            [user.email])
    email.content_subtype = 'html'
    return email
