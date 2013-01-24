# Create your views here.

import json
from django.http import HttpResponse
from django.template import Context, loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from browser import Browser

br = Browser()

def index(request, gag_id='4863604'):
    br.open_gag(int(gag_id))
    gag_img_title, _, _, _ = br.get_info_pad()
    gag_img_url = br.get_image_url()
    streams = br.get_comments()
    gag_comments = []
    for sid, stream in enumerate(streams):
        for rid, reply in enumerate(stream):
            gag_comments.append({'is_lead': rid == 0, 
                                 'uid': reply['uid'],
                                 'content': reply['content'],
            })
    resp_dict = {
        'gag_img_title': gag_img_title,
        'gag_img_url': gag_img_url,
        'gag_comments': gag_comments,
    }
    return render_to_response('captain_obvious.html', resp_dict)

def graph_comment(request):
    uid = request.GET.get('uid', False)
    profile = br.get_fb_profile(uid)
    name = br.get_fb_name(uid)
    return HttpResponse(json.dumps({'uid': uid, 'profile': profile, 'name': name}))

