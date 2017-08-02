from surveys.models import AmbassadorSurvey, TuteeSurvey
from collections import OrderedDict
from django.utils import timezone

def get_survey_stats_for_ambassador(sessions):
    all_surveys = AmbassadorSurvey.objects.filter(
            individual_session__session__in=sessions,
            individual_session__session_date__lte=timezone.now())
    tut_surveys = TuteeSurvey.objects.filter(
            individual_session__session__in=sessions,
            individual_session__session_date__lte=timezone.now())
    cd = OrderedDict()
    for sess in sessions:
        ind = OrderedDict()
        expected = all_surveys.filter(
                individual_session__session=sess)
        completed = expected.filter(submitted=True).count()
        tut_expected = tut_surveys.filter(
                individual_session__session=sess)
        tut_completed = tut_expected.filter(submitted=True).count()
        ind['Total Ambassador Surveys Expected'] = expected.count()
        ind['Ambassador Surveys Received'] = completed
        ind['Total Tutee Surveys Expected'] = tut_expected.count()
        ind['Tutee Surveys Received'] = tut_completed
        if expected.count() > 0:
            ind['Ambassador Completion Rate'] = "{:1.2f} %".format((completed / expected.count()) * 100) 
        else:
            ind['Ambassador Completion Rate'] = "No surveys expected"
        if tut_expected.count() > 0:
            ind['Tutee Completion Rate'] = "{:1.2f} %".format((tut_completed / tut_expected.count()) * 100) 
        else:
            ind['Tutee Completion Rate'] = "No surveys expected"
        cd[sess] = ind
    return cd

