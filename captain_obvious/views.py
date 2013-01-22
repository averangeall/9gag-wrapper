# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse
from browser import Browser

br = Browser()

def index(request, gag_id='4863604'):
    br.open_gag(int(gag_id))
    gag_img_url = br.get_image_url()
    streams = br.get_comments()
    gag_comments = []
    for sid, stream in enumerate(streams):
        for rid, reply in enumerate(stream):
            gag_comments.append({'is_lead': rid == 0, 
                                 'img_url': reply['profile_pic_url'],
                                 'name': reply['user_name'],
                                 'content': reply['content'],
            })
    t = loader.get_template('captain_obvious.html')
    c = Context({
        'gag_img_url': gag_img_url,
        'gag_comments': gag_comments,
    })
    return HttpResponse(t.render(c))
