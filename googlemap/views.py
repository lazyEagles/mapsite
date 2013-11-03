# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, RequestContext
from django.core.context_processors import csrf
#from django.template import RequestContext
from googlemap.models import Cityinfo
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def index(request):
    cities = Cityinfo.objects.raw('SELECT * FROM cityinfo')
    return render_to_response('googlemap/index.html',{
        'cities': cities,
    })

def readme(request):
    return render_to_response('googlemap/readme.html',{
    })

def query(request):
    return render_to_response('googlemap/query.html',{
    })

@csrf_exempt
#@csrf_protect
def region(request):
#    c = {}
#    c.update(csrf(request))

    minlog = request.POST['minlog']
    minlat = request.POST['minlat']
    maxlog = request.POST['maxlog']
    maxlat = request.POST['maxlat']

    request.session['minlog'] = minlog
    request.session['minlat'] = minlat
    request.session['maxlog'] = maxlog
    request.session['maxlat'] = maxlat

    cities = Cityinfo.objects.raw('SELECT * FROM cityinfo WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)',[minlog,minlat,maxlog,maxlat])

    return render_to_response('googlemap/region.html',{
        'cities': cities,
        'minlog': minlog,
        'minlat': minlat,
        'maxlog': maxlog,
        'maxlat': maxlat,
    },context_instance=RequestContext(request))

@csrf_exempt
def distance(request):
    minlog = request.session['minlog']
    minlat = request.session['minlat']
    maxlog = request.session['maxlog']
    maxlat = request.session['maxlat']
    citynames = []

    region_cities = Cityinfo.objects.raw('SELECT * FROM cityinfo WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)',[minlog,minlat,maxlog,maxlat])

    for city in region_cities:
        citynames.append(city.cityname)

    citynames = set(citynames)

    c1 = ""
    c2 = ""
    distance = ""
    if request.method == 'POST':
        c1 = request.POST['city1']
        c2 = request.POST['city2']
        distance = Cityinfo.objects.raw('''
            SELECT city1.cityname, 
                   city2.cityname As city2_name, 
                   ST_Distance_Sphere(city1.geom, city2.geom) As distance_cities 
            FROM (SELECT * FROM cityinfo WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) city1, 
                 (SELECT * FROM cityinfo WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) city2 
            WHERE city1.cityname = %s AND city2.cityname = %s
            ''',[minlog, minlat, maxlog, maxlat, minlog, minlat, maxlog, maxlat, c1, c2])

    return render_to_response('googlemap/distance.html',{
        'c1': c1,
        'c2': c2,
        'distance': distance,
        'citynames': citynames,
    },context_instance=RequestContext(request))

@csrf_exempt
def country(request):
    minlog = request.session['minlog']
    minlat = request.session['minlat']
    maxlog = request.session['maxlog']
    maxlat = request.session['maxlat']
    countries = []

    region_cities = Cityinfo.objects.raw('SELECT * FROM cityinfo WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)',[minlog,minlat,maxlog,maxlat])

    for city in region_cities:
        countries.append(city.countryname)

    countries = set(countries)

    cities = ""
    if request.method == 'POST':
        country1 = request.POST['country1']
        if country1 == "All Countries":
            cities = Cityinfo.objects.raw('''
                 SELECT *
                 FROM 
                     (SELECT * FROM cityinfo 
                      WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) As ci1
                ''', [minlog, minlat, maxlog, maxlat])
        else:
            cities = Cityinfo.objects.raw('''
                 SELECT *
                 FROM 
                     (SELECT * FROM cityinfo 
                      WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) As ci1
                 WHERE countryname = %s
                ''',[minlog, minlat, maxlog, maxlat, country1])

    return render_to_response('googlemap/country.html',{
        'cities': cities,
        'countries': countries,
    },context_instance=RequestContext(request))


@csrf_exempt
def population(request):
    minlog = request.session['minlog']
    minlat = request.session['minlat']
    maxlog = request.session['maxlog']
    maxlat = request.session['maxlat']
    populations = []

    region_cities = Cityinfo.objects.raw('SELECT * FROM cityinfo WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)',[minlog,minlat,maxlog,maxlat])

    for city in region_cities:
        populations.append(city.populationclass)

    orders = {'Less than 50,000': 1, '50,000 to 100,000': 2, '100,000 to 250,000': 3, '250,000 to 500,000': 4, '500,000 to 1,000,000': 5, '1,000,000 to 5,000,000': 6, '5,000,000 and greater': 7}
    populations = sorted(set(populations), key=orders.__getitem__)

    cities = ""
    if request.method == 'POST':
        population1 = request.POST['population']
        if population1 == "All Population Classes":
            cities = Cityinfo.objects.raw('''
                SELECT *
                FROM
                    (SELECT * FROM cityinfo
                     WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) As ci1
                ''',[minlog, minlat, maxlog, maxlat])            
        else:
            cities = Cityinfo.objects.raw('''
                SELECT *
                FROM
                    (SELECT * FROM cityinfo
                     WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) As ci1
                WHERE populationclass = %s
                ''',[minlog, minlat, maxlog, maxlat, population1])

    return render_to_response('googlemap/population.html',{
        'cities': cities,
        'populations': populations,
    }, context_instance=RequestContext(request))

@csrf_exempt
def neighbor(request):
    minlog = request.session['minlog']
    minlat = request.session['minlat']
    maxlog = request.session['maxlog']
    maxlat = request.session['maxlat']
    citynames = []

    region_cities = Cityinfo.objects.raw('SELECT * FROM cityinfo WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)',[minlog,minlat,maxlog,maxlat])

    for city in region_cities:
        citynames.append(city.cityname)

    citynames = set(citynames)

    cities = ""
    if request.method == 'POST':
        city1 = request.POST['city1']
        n_neighbor = request.POST['n_neighbor']
        cities = Cityinfo.objects.raw('''
            SELECT ci1.cityname, ci2.cityname As neighbor, 
                   ci2.countryname As neighbor_country, 
                   ST_Distance_Sphere(ci1.geom, ci2.geom) As distance 
            FROM 
                (SELECT * FROM cityinfo 
                 WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) As ci1, 
                (SELECT * FROM cityinfo 
                 WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)) As ci2 
            WHERE ci1.cityname = %s and ci1.cityname <> ci2.cityname 
            ORDER BY ST_Distance_Sphere(ci1.geom, ci2.geom) LIMIT %s
            ''', [minlog, minlat, maxlog, maxlat, minlog, minlat, maxlog, maxlat, city1, n_neighbor]
        )

    return render_to_response('googlemap/neighbor.html',{
        'cities': cities,
        'citynames': citynames,
    }, context_instance=RequestContext(request))
