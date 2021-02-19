import os, json

from .models import Country, State, City

def import_world_data():
    world_json = os.path.join(os.getcwd(), 'countries+states+cities.json')
    with open(world_json) as f:
        world_data = json.load(f)
        for country in world_data:
            if country['id']==101: #(for India) if you need all country dount use this
                print(country['name'])
                country_data = Country.objects.create(
                id = country['id'],
                name = country['name'],
                iso3 = country['iso3'],
                iso2 = country['iso2'],
                phone_code = country['phone_code'],
                capital = country['capital'],
                currency = country['currency']
            )
                for state in country['states']:
                    print(state['name'])
                    state_data = State.objects.create(
                    country = Country.objects.get(pk=country['id']),
                    id = state['id'],
                    name = state['name'],
                    state_code = state['state_code']
                )
                    for city in state['cities']:
                        print(city['name'])
                        city_data = City.objects.create(
                        state = State.objects.get(pk=state['id']),
                        id = city['id'],
                        name = city['name'],
                        latitude = city['latitude'],
                        longitude = city['longitude']
                    )