from availabilities.models import Availability

def update_other_times(availability):
    availability.room_available = False
    availability.save()
    # everythin will need to be updated
    if availability.semester.term == 'SC':
        qs = Availability.objects.filter(
                                        is_scheduled = False,
                                        start_time = availability.start_time,
                                        end_time = availability.end_time,
                                        day = availability.day,
                                        room_available=True)
    else:
        qs = Availability.objects.filter(
                                        is_scheduled = False,
                                        start_time = availability.start_time,
                                        end_time = availability.end_time,
                                        day = availability.day,
                                       semester = availability.semester,
                                        room_available=True)
    for q in qs:
        q.room_available = False
        q.save()
