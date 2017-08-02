'''
Idea:
    Create a random collection of sessions & surveys for an entire semester.
How:
    1. Create a date range.
    2. Create a fixed number of sessions for that date range.
        2a. Pick tutee at random.
        2b. Pick ambassador at random.
        2c. Pick course at random.
        2d. Pick time at random. ( Need to create an availability probably )
    3. Create individual sessions for each session created.
    4. Create ambassador and tutee surveys for each individual session.
    5. Randomly fill out all surveys.
'''
import random
from datetime import time
from django.contrib.auth.models import User
from availabilities.models import Availability
from rquests.models import TutoringRequest
from semesters.models import Semester
from surveys.models import AmbassadorSurvey, TuteeSurvey
from tutoring_sessions.models import ROOMS, Session, IndividualSession
from courses.models import Course

# we are currently in the summer so we will do it for summer c
# Gonna just use the preexisting model in the DB
semester = Semester.objects.get(term = 'SC')
start = semester.start_date
end = semester.end_date
TOTAL_SESSIONS = 20
random.seed()

def run():
    for x in range(TOTAL_SESSIONS):
        HOUR = random.randint(7, 18)
        stime = time(HOUR, 0, 0)
        etime = time(HOUR+1, 0, 0)
        tutees = User.objects.exclude(email__in=["", None], 
                username__in=['GROUP_USER', 'TEMP_USER', 'testphd', 'mherlle'],
                is_active=False,
                is_staff=True)
        tcount = tutees.count()
        tut = tutees[random.randint(0, tcount-1)]
        day = random.randint(1, 5)
        courses = Course.objects.exclude(team=None)
        csize = courses.count()
        c = courses[random.randint(0, csize-1)]
        tsize = c.team.count()
        amb = c.team.all()[random.randint(0, tsize-1)]
        info = make_request(tut, amb, stime, etime, day, c)
        print("Request : {}\nAvailability : {}".format(info['request'], info['availability']))
        sessions = create_session(info)
        print("Sessions : {}", sessions)
        asurvs = AmbassadorSurvey.create_surveys_from_individual_sessions(sessions)
        tsurvs = TuteeSurvey.create_surveys_from_individual_sessions(sessions)
        complete_surveys(asurvs, tsurvs)
        if x == 15:
            HOUR = random.randint(7, 18)
            stime = time(HOUR, 0, 0)
            etime = time(HOUR+1, 0, 0)
            amb = c.team.all()[random.randint(0, tsize-1)]
            info = make_request(tut, amb, stime, etime, day, c)
            print("Request : {}\nAvailability : {}".format(info['request'], info['availability']))
            sessions = create_session(info)
            print("Sessions : {}", sessions)
            asurvs = AmbassadorSurvey.create_surveys_from_individual_sessions(sessions)
            tsurvs = TuteeSurvey.create_surveys_from_individual_sessions(sessions)
            complete_surveys(asurvs, tsurvs)



absent = [True, False]

def complete_surveys(asurvs, tsurvs):
    for surv in asurvs:
        surv.rating_1 = random.randint(1,5)
        surv.rating_2 = random.randint(1,5)
        surv.rating_3 = random.randint(1,5)
        surv.submitted = True
        surv.session_canceled = False
        surv.tutee_absent = absent[random.randint(0,1)]
        surv.comments = "Lorem ipsum dolor sit"
        surv.save()
    for surv in tsurvs:
        if AmbassadorSurvey.objects.get(
                individual_session=surv.individual_session
                ).tutee_absent:
            surv.tutee_absent = True
            surv.submitted = True
            surv.save()
        else:
            surv.rating_1 = random.randint(1, 5)
            surv.rating_2 = random.randint(1, 5)
            surv.rating_3 = random.randint(1, 5)
            surv.rating_4 = random.randint(1, 5)
            surv.rating_5 = random.randint(1, 5)
            surv.rating_6 = random.randint(1, 5)
            surv.rating_7 = random.randint(1, 5)
            surv.comments = "Lorem ipsum dolor sit amet"
            surv.submitted = True
            surv.wearing_shirt = True
            surv.save()


def make_request(tut, amb, stime, etime, day, c):
    ava = Availability.objects.create(
            ambassador = amb,
            semester = semester,
            start_time = stime,
            end_time = etime,
            day = day,
            is_scheduled = True,
            )
    req = TutoringRequest.objects.create(
            submitted_by = tut,
            availability = ava,
            course = c,
            submitted_at = start,
            updated_at = start,
            )
    return {'request' : req, 'availability' : ava}

def create_session(info):
    dates = Session.make_dates(info['request'])
    session = Session()
    session.room_number = '101A'
    session.ambassador = info['availability'].ambassador
    session.start_time = info['availability'].start_time
    session.end_time = info['availability'].end_time
    session.day_of_week = info['availability'].day
    session.start_date = dates[0]
    session.end_date = dates[-1]
    session.tutee = info['request'].submitted_by
    session.course = info['request'].course
    session.availability = info['availability']
    session.save()
    sessions = IndividualSession.make_from_dates(session, dates)
    return sessions

