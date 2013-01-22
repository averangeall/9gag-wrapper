# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    t = loader.get_template('captain_obvious.html')
    gag_comments = []
    gag_comments.append({'is_lead': True, 
                         'img_url': 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/41630_100001616821682_8165_q.jpg',
                         'name': 'John Lin',
                         'content': 'Hello',
    })
    gag_comments.append({'is_lead': False, 
                         'img_url': 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash4/371623_100000551347790_1436916040_q.jpg',
                         'name': 'Emil Ferent',
                         'content': 'Yo',
    })
    gag_comments.append({'is_lead': True, 
                         'img_url': 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/41630_100001616821682_8165_q.jpg',
                         'name': 'John Lin',
                         'content': 'Hello again',
    })
    c = Context({
        'gag_img_url': 'http://d24w6bsrhbeh9d.cloudfront.net/photo/4863604_700b_v2.jpg',
        'gag_comments': gag_comments,
    })
    return HttpResponse(t.render(c))
