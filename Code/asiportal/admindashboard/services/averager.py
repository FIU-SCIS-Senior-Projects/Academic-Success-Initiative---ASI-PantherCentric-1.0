from collections import defaultdict
# this is bad we will make it general
def gather_context(sessions):
    context = dict()
    for session in sessions:
        inds = session.individual_sessions.all()
        ambs = [ind.surveys_ambassadorsurvey_related.get() for ind in inds]
        tuts = [ind.surveys_tuteesurvey_related.get() for ind in inds]
        both = zip(ambs, tuts)
        context[session.__str__()] = {
                'surveys' : both,
                'overall_ambassador' : overall_averages(
                    ambs,
                    **{
                        "Student Has Made Great Progress During Session" : 'rating_1',
                        "Student Shows Good Study Skills" : 'rating_2',
                        "Student Came Prepared for Session" : 'rating_3',
                        }).items,
                'overall_tutee' : overall_averages(tuts,
                    **{
                        "It is clear the ambassador knows and understands the subject matter of this course" : 'rating_1',
                        "The ambassador explains ideas and concepts clearly." : 'rating_2',
                        "The ambassador asks me questions and has me work sample problems." : 'rating_3',
                        "The ambassador listens to me and tries to understand my problems." : 'rating_4',
                        "The ambassador is friendly and courteous with me." : 'rating_5',
                        "The ambassador is trying to accommodate my learning style." : 'rating_6',
                        "The session is helpful and improved my understanding of the subject." : 'rating_7',
                    }
                    ).items,
                'total_absences' : calculate_total_absences(ambs),
                }
    return context

def calculate_total_absences(surveys):
    total_absences = 0
    total_sessions = 0
    for survey in surveys:
        total_absences = total_absences + 1 if survey.tutee_absent and not survey.session_canceled else total_absences
        total_sessions = total_sessions + 1 if not survey.session_canceled else total_sessions
    return {
            'absences' : total_absences,
            'total_sessions' : total_sessions }

'''
overall_averages(objects, **fields)
    a method which takes a list of objects and a dict of names -> fields
    which computes the average of the given fields contained in the list.

objects -- a list of models / objects to iterate through.
This could work with any model so long as the fields are integer / float value

**fields -- this is a dict which is of the format
{ "name_of_average" : "field_name" }
The key value will be the key for the result in the returned dictionary.

The return value of this function is a dictionary of the form

{ "name_of_average" : result }
'''
def overall_averages(objects, **fields):
    total_objects= len(objects)
    avgs = defaultdict(int)

    if total_objects is 0:
        for key, value in fields.items():
            avgs[key] = 0
        avgs['errors'] = True
        avgs['message'] = "No surveys to average."
        return avgs

    for obj in objects:
        for key, value in fields.items():
            avgs[key] += obj.__getattribute__(value) / total_objects
    return avgs
