# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Compatibility
import facebook
import urllib2
from urllib2 import urlparse
from itertools import chain
from functools import partial
from simplejson import dumps

CLIENT = "205425319498174"
REDIRECT = "http://localhost:8000/landing"
SECRET = "1a5aa67a3a7f8bbe40422a8d01445e82"

JASON_CODE = "P-tmQQWr3TWm8y3MXPF6oTY1VP2hO2j_iEwAcrhcJs0.eyJpdiI6IkhJQWhXSHMyQWFwaGVDX3c4alc5dUEifQ.M-xyyRQs6IliFIJE8kduuQgtfOAANaQqlZMkkIMbGcpKuYf5x5MjmyBNpOJ2GVzLjtnVeljj89RXaZt8G1aZsqXMY1QzMenxo3PyAh2cunz9gfqMaiD-j3Ml46U5fa5XOgzFTcdBiJ5ziHPARpo7Ig"

#return HttpResponse("Hello, world. You're at the poll index.")

def auth(request):
    return render_to_response('auth.html')

def set_compatibility(request):
    get = request.GET;



    rating, f1_id = int(get['rating']), get['f1_id']
    f2_id, rater = get['f2_id'], get['rater']
    f1_name, f2_name = get['f1_name'], get['f2_name']
    rater_name = get['rater_name']

    c = Compatibility(rating=rating, f1_id=f1_id, f2_id=f2_id, rater=rater,
                      f1_name=f1_name, f2_name=f2_name, rater_name=rater_name)
    c.save()

    return HttpResponse("okay");

def get_agg_rating(f1_id, f2_id):
    objs = chain(Compatibility.objects.filter(f1_id=f1_id, f2_id=f2_id),
                 Compatibility.objects.filter(f1_id=f2_id, f2_id=f1_id))
    objs = [o for o in objs]
    ratings = [o.rating for o in objs]
    raters = [[o.rater,o.rater_name] for o in objs]
    if ratings:
        return {'rating': sum(ratings) / float(len(ratings)), 'raters': raters}
    else: return None

def get_people(me_id):
    #objs = map(lambda o: o.f2_id, Compatibility.objects.filter(f1_id=me_id))
    #objs += map(lambda o: o.f1_id, Compatibility.objects.filter(f2_id=me_id))
    #objs = set(objs)

    objs = map(lambda o: "%d,%s" % (o.f2_id, o.f2_name), Compatibility.objects.filter(f1_id=me_id))
    objs += map(lambda o: "%d,%s" % (o.f1_id, o.f1_name), Compatibility.objects.filter(f2_id=me_id))
    objs = set(objs)


    info = map(partial(get_agg_rating, me_id), [o.split(",")[0] for o in objs])
    return zip(objs, info)

def get_people_json(me_id):
    d = [{'match_id': match_id.split(",")[0],
          'match_name': match_id.split(",")[1],
          'rating': rating_info['rating'],
          'raters': rating_info['raters']}
          for match_id, rating_info in get_people(me_id)]
    return dumps(d, indent=4)


def ajax_matches(request):
    return HttpResponse(get_people_json(request.GET['fid']), mimetype='application/json')

def matches(request):
    return render_to_response('matches.html')

def landing(request):
    return render_to_response('landing.html')
def landing_live(request):
    return render_to_response('landing_live.html')


# DEPRECATED
def get_access_token(code):
    url = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (CLIENT, REDIRECT, SECRET, JASON_CODE)
    resp = urllib2.urlopen(url)
    params = resp.read()


