from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from tutoring_sessions.models import Session
from asiapp.services import account_emailer
from collections import defaultdict
from datetime import date
from django.core import mail

class Command(BaseCommand):
    help = 'Sends a reminder to tutees about their sessions for that day'

    def handle(self, *args, **options):

        sessions = Session.objects.filter(day_of_week=date.today().isoweekday())
        daily = defaultdict(list)
        for session in sessions:
            daily[session.tutee] +=  [session] if session.end_date >= date.today() else []
        messages = []

        for key in daily:
            messages += [account_emailer.send_reminder(key, daily[key], date.today())]

        connection = mail.get_connection()
        connection.send_messages(messages)
