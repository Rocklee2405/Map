import requests
import json


link_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
keyword = "coffee"
location = "10.8047203,106.7167155"
radius = "2000"


def get_api():
    with open("API_key.txt", "rt") as f:
        data = f.read()
    return data


def find_beer(keyword, location, radius):
    result = []
    dict_data = {"keyword": keyword,
                 "location": location,
                 "radius": radius,
                 "key": get_api()}
    ses = requests.Session()
    reps = ses.get(link_url, params=dict_data)
    if reps.status_code // 100 == 5:
        raise Exception("Cannot connect to server!")
    data = reps.json()
    if not data:
        raise ValueError("Not found data!")
    result.extend(data['results'])
    return result


def create_geojson(coffee):
    geojson_feature = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(data['geometry']['location']['lng']),
                                float(data['geometry']['location']['lat'])]},
            "properties": {"name": data["vicinity"]},
        } for data in coffee]
    geojon_result = {"type": "FeatureCollection",
                     "features": geojson_feature}
    with open("coffee.geojson", "wt", encoding="utf-8") as f:
        json.dump(geojon_result, f, ensure_ascii=False, indent=4)


def main():
    result = find_beer(keyword, location, radius)
    create_geojson(result)


if __name__ == "__main__":
    main()
