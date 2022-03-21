from calendar import c
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=961444a973aab50a93944c84de64389d'

    cities = City.objects.all() #return all the cities in the database

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    
    form = CityForm()

    weather_data = []

    for city in cities:
        try:
            city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types format is allowing us to insert any city we want
            
            weather = {
                'city': city,
                'temp': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
        
            weather_data.append(weather)
        except:
            print("please input valid city")

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context) #returns the index.html template
