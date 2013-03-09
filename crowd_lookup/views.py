# Create your views here.

import json
from django.http import HttpResponse

def get_recomm_words(request, gag_id):
    words = []
    words += ['Infantiles', 'Equipment', 'Juegos', 'Equipes', 'Para']
    return HttpResponse(json.dumps(words))

def query_word(request):
    gag_id = request.GET.get('gag_id', False)
    word = request.GET.get('word', False)
    definitions = []
    definitions.append({'type': 'text', 'src': 'oxford', 'content': 'This is a book.'})
    definitions.append({'type': 'video', 'src': 'youtube.com', 'content': 'http://www.youtube.com/watch?v=WD2WffuzZmI'})
    return HttpResponse(json.dumps(definitions))
