# Create your views here.

import re
import json
import urllib
from django.http import HttpResponse
from django.template import Context, loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from browser import Browser
from memeclass import MemeClassifier

br = Browser()
mc = MemeClassifier('static/meme-templates')

gag_img_urls = {}

def index(request, gag_id='6400621'):
    br.open_gag(int(gag_id))
    gag_img_title = br.get_title()
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
        'gag_id': gag_id,
        'gag_img_title': gag_img_title,
        'gag_img_url': gag_img_url,
        'gag_comments': gag_comments,
    }
    gag_img_urls[gag_id] = gag_img_url
    return render_to_response('captain_obvious.html', resp_dict)

def graph_comment(request):
    uid = request.GET.get('uid', False)
    profile = br.get_fb_profile(uid)
    name = br.get_fb_name(uid)
    return HttpResponse(json.dumps({'uid': uid, 'profile': profile, 'name': name}))

def meme_class(request):
    gag_id = request.GET.get('gag_id', False)
    if gag_id in gag_img_urls:
        gag_img_url = gag_img_urls[gag_id]
    else:
        br.open_gag(int(gag_id))
        gag_img_url = br.get_image_url()
    gag_fname = "/tmp/" + gag_id + ".jpg"
    urllib.urlretrieve(gag_img_url, gag_fname)
    meme_class = mc.classify(gag_fname)
    if meme_class != None:
        meme_class = meme_class[meme_class.rfind('/') + 1 : meme_class.rfind('.')]
        meme_class = re.sub('-', ' ', meme_class)
    return HttpResponse(json.dumps({'gag_id': gag_id, 'meme_class': meme_class}))

