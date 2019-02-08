#!/usr/bin/python

from utils import read_papers
from urllib.request import urlopen
import os
import unidecode
import json
import config


def get_locations():

    # Get papers
    papers = read_papers()
    # Get authors' locations
    locations = []
    for paper in papers:
        universities = [ author.split(':')[1] for author in paper['author_names'] ]
        for uni in universities:
            locations.extend([ u.strip() for u in uni.split('/') ])
    return set(locations)


def save_geo_locations(locations):
    
    for location in locations:
        filename = os.path.join('data', 'locations', location + '.json')
        if not os.path.isfile(filename):
            address_no_blanks = unidecode.unidecode(location).replace(' ', '+')
            url = config.GOOGLE_BASE_URL.format(address_no_blanks, config.GOOGLE_API_KEY)
            print('Calling: {}'.format(url))
            response = urlopen(url)
            json_geocode = response.read()
            with open(filename, 'wb') as outfile:
                outfile.write(json_geocode)


def get_coordinates(filename):

    data = json.load(open(filename))
    geometry = data['results'][0]['geometry']
    loc = geometry['location']

    return [ loc['lng'], loc['lat'] ]


def geo_data():
    """ Create GeoJSON file """

    # http://geojson.org/
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }

    directory = os.path.join('data', 'locations')

    for filename in os.listdir(directory):
        
        coordinates = get_coordinates(os.path.join(directory, filename))
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": coordinates,
            },
            "properties": {
                "name": filename.split('.json')[0]
            }
        }
        geo_data['features'].append(feature)

    return geo_data


def collab_data():

    # Get papers
    papers = read_papers()

    # http://geojson.org/
    collab_data = {
        "type": "FeatureCollection",
        "features": []
    }

    directory = os.path.join('data', 'locations')

    # Get collaborations
    for paper in papers:
        # Universities
        universities = [ author.split(':')[1] for author in paper['author_names'] ]
        collaboration = []
        for uni in universities:
            collaboration.extend([ u.strip() for u in uni.split('/') ])
        collaboration = list(set(collaboration))
        # Feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [ get_coordinates(os.path.join(directory, uni + '.json')) for uni in collaboration ],
            },
            "properties": {
                "name": '{}. {} ({})'.format(paper['number'], paper['title'], paper['type'])
            }
        }
        collab_data['features'].append(feature)

    return collab_data


def get_country(country):

    if country == 'USA' or country == 'United States': country = 'United States of America'
    elif country == 'UK': country = 'United Kingdom'
    elif country == 'Hong Kong': country = 'China'
    elif country == 'Serbia': country = 'Republic of Serbia'
    elif 'Singapore' in country: country = 'Malaysia'
    return country


def get_countries_data():

    # Read countries
    geometries = {}
    filename = os.path.join("data", "countries.geojson")
    data = json.load(open(filename))
    for feature in data['features']:
        name = feature['properties']['name']
        geometry = feature['geometry']
        geometries[name] = geometry

    # Get papers
    papers = read_papers()

    # Directory for locations data
    directory = os.path.join('data', 'locations')

    # http://geojson.org/
    countries_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Get authors and universities
    densities = {}
    for paper in papers:
        # Get authors
        for author, unis in [ author.split(':') for author in paper['author_names'] ]:
            # Get country per university
            universities = [ u.strip() for u in unis.split('/') ]
            for uni in universities:
                # Get uni's geometry
                filename = os.path.join('data', 'locations', uni + '.json')
                data = json.load(open(filename))
                address = data['results'][0]['formatted_address']
                country = get_country(address.split(',')[-1].strip())
                if country not in geometries:
                    raise Exception('Country {} not found in the file with coordinates'.format(country))
                # Add density for each country
                densities.setdefault(country, set())
                densities[country].add(author)

    for country in densities:
        # Get geometry
        geometry = geometries[country]
        feature = {
            "type": "Feature",
            "geometry": geometry,
            "properties": {
                "name": country,
                "density": len(densities[country])
            }
        }
        countries_data['features'].append(feature)

    return countries_data


if __name__ == '__main__':
    
    # Get locations
    locations = sorted(get_locations())
    # Save GEO data
    save_geo_locations(locations)