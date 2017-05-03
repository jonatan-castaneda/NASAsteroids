from django.shortcuts import render
import requests
import datetime
import json

# Create your views here.
def index(request):
    if request.method == 'POST':
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')

        payload = {
            'start_date':date_start,
            'end_date':date_end,
            'api_key':'o1QgL2TMcivKCABk2hqoZmxgCOkMoFspxtgkDoIK'
            }
        r = requests.get("https://api.nasa.gov/neo/rest/v1/feed", params=payload)
        json_str = json.loads(r.text)
        asteroids = []
        try:
            for key,value in json_str['near_earth_objects'].items():
                for asteroid in json_str['near_earth_objects'][key]:
                    a={
                        'name':asteroid['name'],
                        'diameter_min':asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
                        'diameter_max':asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                        'url':asteroid['nasa_jpl_url'],
                        'dangerous':asteroid['is_potentially_hazardous_asteroid'],
                        'date':key
                    }
                    asteroids.append(a)
        except:
            asteroids.append({'error':'Intenta cargar de nuevo la página o verifica los datos proporcionados'})
    else:
        yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
        yest = yesterday.strftime("%Y-%m-%d")
        #print("https://api.nasa.gov/neo/rest/v1/feed?start_date=%s&end_date=%s&api_key=o1QgL2TMcivKCABk2hqoZmxgCOkMoFspxtgkDoIK" % ( yest, yest ))
        payload = {
            'start_date':yest,
            'end_date':yest,
            'api_key':'o1QgL2TMcivKCABk2hqoZmxgCOkMoFspxtgkDoIK'
            }
        r = requests.get("https://api.nasa.gov/neo/rest/v1/feed", params=payload)
        json_str = json.loads(r.text)
        asteroids = []
        try:
            for key,value in json_str['near_earth_objects'].items():
                for asteroid in json_str['near_earth_objects'][key]:
                    a={
                        'name':asteroid['name'],
                        'diameter_min':asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
                        'diameter_max':asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                        'url':asteroid['nasa_jpl_url'],
                        'dangerous':asteroid['is_potentially_hazardous_asteroid'],
                        'date':key
                    }
                    asteroids.append(a)
        except:
            asteroids.append({'error':'Intente hacer de nuevo la petición o verifique los datos proporcionados'})
        
    return render(request,"landing/index.html",{'asteroids':asteroids})
