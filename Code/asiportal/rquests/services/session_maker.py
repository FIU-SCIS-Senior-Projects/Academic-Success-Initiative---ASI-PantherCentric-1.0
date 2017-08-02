from datetime import timedelta, datetime
from tutoring_sessions.models import Session
from django.utils import timezone

def create_session(form):
        request = form.save()
        session = Session()
        session.tutoring_request = request
        session.room_number = form.cleaned_data['room_number']
        session = make_dates(session)
        return session

def make_dates(session):
    availability = session.tutoring_request.availability
    updated_at = session.tutoring_request.updated_at
    if isinstance(updated_at, datetime):
        updated_at = updated_at.date()
    semester = availability.semester
    start_diff =  availability.day - updated_at.isoweekday()
    end_diff = availability.day - semester.end_date.isoweekday() 
    # the last session should take place on the week before
    # the last week of the semester on the correct availability day
    if updated_at < semester.start_date:
        session.start_date = semester.start_date + timedelta(weeks=1,days=start_diff)
        session.end_date = semester.end_date - timedelta(weeks=1,days=end_diff)
    else:
        session.start_date = updated_at + timedelta(weeks=1, days=start_diff)
        session.end_date = semester.end_date - timedelta(weeks=1,days=end_diff)
    return session


