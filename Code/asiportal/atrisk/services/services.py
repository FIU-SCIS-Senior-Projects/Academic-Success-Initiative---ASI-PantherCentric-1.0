from atrisk.models import AltUser
import requests
import json
from django.utils import timezone
api_secret = '3ab4f05a44abd335fa9dcb9118898329'
end_point = 'https://mixpanel.com/api'
version = '2.0'

def get_stats(title):
    now = str(timezone.now().date())
    rqtype = 'segmentation'
    params = {'event' : 'Watched Video {}'.format(title),
            'type' : 'general',
            'limit' : 150,
            'on' : 'user["Who"]',
            'to_date': now,
            'from_date' : '2017-01-01',
            'unit' : 'day',
            }
    url = '/'.join([end_point, version, rqtype])
    data = requests.get(
            url,
            auth=(api_secret,''),
            params=params)
    thangs = data.json()
    data = thangs.get('data')
    sums = 0
    stats = dict()
    for i,j in data.get("values").items():
        stats[i] = j
    tots = dict()
    for x, y in stats.items():
        tots[x] = sum(y.values())
    return {'stats' : stats, 'totals' : tots, 'debug' : params}

def is_atrisk(user):
    return AltUser.objects.filter(username=user).exists()
