import requests


def fetch_location(address):
    query = {'address': address, 'sensor': False}
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=query).json()

    if r['status'] == 'OK':
        rs = r['results'][0]
        gm = rs['geometry']
        location = gm['location']
    else:
        location = None

    return location
