from apiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

def send_invite(session):
    scopes = ['https://www.googleapis.com/auth/calendar']

    # You're gonna need this file from someone who has it
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/jake/asi_app/asiportal/asiportal/rquests/services/keyfile.json',
            scopes)


    delegated_credentials = credentials.create_delegated('jakedlopez@gmail.com')

    http_auth = credentials.authorize(Http())

    calendar = build('calendar', 'v3', http=http_auth)

    event = {
            'summary' : "{} Tutoring".format(session.course),
            'location' : 'PG-6 Room 100',
            'description' : '{} tutoring with {}'.format(session.course, session.ambassador.get_full_name()),
            'start' : {
                'dateTime' : "{}T{}-04:00".format(session.start_date, session.start_time),
                'timeZone' : 'America/New_York',
                },
            'end' : {
                'dateTime' : '{}T{}-04:00'.format(session.start_date, session.end_time),
                'timeZone' : 'America/New_York',
                },

            # no hyphens for the date
            'recurrence' : ['RRULE:FREQ=WEEKLY;UNTIL={}T170000Z'.format(str(session.end_date).replace('-', ''))],
            'attendees' : [
                { 'email' : 'jakedlopez@gmail.com' }, 
                {'email' :  'jake.lopez001@mymdc.net',    # dont want to upset anyone with actual emails and invites right now ,
                    'responseStatus' : 'needsAction',
                    'displayName' : '{}'.format(session.tutee.get_full_name()) },
                ],
            'reminders' : { 'useDefault' : True, },
            }
    event = calendar.events().insert(calendarId="primary", body=event, sendNotifications=True).execute()
    print("Event created : {}".format(event.get('htmlLink')))
