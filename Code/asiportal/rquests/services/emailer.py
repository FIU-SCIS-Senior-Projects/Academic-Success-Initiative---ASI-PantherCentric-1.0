from django.core.mail import EmailMessage
from django.template.loader import get_template

def no_room_available_email(request):
    title = '[ASI] Tutoring Request Unable To Be Scheduled'
    email_template = get_template('no_room_available.txt')
    email_context = {'firstName' : request.submitted_by.first_name,
                     'courseID' : request.course,
                     'start' : request.availability.start_time,
                     'end' : request.availability.end_time,
                     }
    message = email_template.render(email_context)
    tutee_email = request.submitted_by.email
    email = EmailMessage(title,message,'asi-noreply@cs.fiu.edu',[tutee_email], bcc=['asisoftwaretest@gmail.com'])
    email.send()


def tutoring_confirmation_email(session):
    title = '[ASI] Scheduled Tutoring Session Confirmation'
    email_template = get_template('session_confirmation.txt')
    email_context = {'firstName': session.tutee.first_name,
                             'courseID': session.course,
                             'day':session.availability.get_day_display(),
                             'startTime': session.availability.start_time,
                             'endTime':session.availability.end_time,
                             'ambassadorName':
                             session.availability.ambassador.get_full_name(),
                             'ambassadorEmail':session.availability.ambassador.email,
                             'startDate':session.start_date.strftime('%B %d, %Y'),
                             'endDate':session.end_date.strftime('%B %d, %Y'),
                             }
    message = email_template.render(email_context)
    tutee_email = session.tutee.email
    ambassador_email = session.availability.ambassador.email
    email = EmailMessage(title,message,'asi-noreply@cs.fiu.edu',[tutee_email, ambassador_email], bcc=['asisoftwaretest@gmail.com'])
    email.send()

def request_submission_email(request):
    title = '[ASI] Tutoring Request Received'
    email_template = get_template('request_confirmation.txt')
    email_context = {
            'tutee_name' : request.submitted_by.get_full_name(),
            'course' : request.course,
            'day' : request.availability.get_day_display(),
            'start_time' : request.availability.start_time.strftime('%-I:%M %p'),
            'end_time' : request.availability.end_time.strftime('%-I:%M %p'),
            'ambassador': request.availability.ambassador.get_full_name(),
            'semester' : request.availability.semester,
            }
    message = email_template.render(email_context)
    tutee_email = request.submitted_by.email
    email = EmailMessage(title,message,'asi-noreply@cs.fiu.edu', [tutee_email], bcc=['asisoftwaretest@gmail.com'])
    email.send()
