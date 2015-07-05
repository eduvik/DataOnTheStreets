import json
import googlemaps
import csv
import math
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

data_file = os.path.join(APP_ROOT, "Outdoor_Furniture.csv")

#gmaps = googlemaps.Client(key='AIzaSyBHrhezRenR1sbHPTxBJTUtyFPtpkcd4wU')
gmaps = googlemaps.Client(key='AIzaSyDjaCfNl8pEPZfKi-Spl-aN8Y9a_7kov0I')



def get_human_readable_address(lat, long):
    int_data = gmaps.reverse_geocode((float(lat), float(long)))

    int_location = None
    for results in int_data:
        if "/" in results["address_components"][0]["long_name"]:
            int_location = results["address_components"][0]["long_name"]
    if int_location is None:
        int_location = int_data[0]["formatted_address"]

    return int_location


def find_object(coord, utility_type, utility_data_filename=data_file, gmaps=gmaps, utility_name_map={"water": "drinking fountain", "toilet": "toilet", "food":"food", "shelter":"shelter"}):
    class FoundObject(object):
        def __init__(self, asset, dist, address):
            self.distance = dist
            self.name = asset[5]
            self.location = asset[8]
            self.address = address
    utility_data = csv.reader(open(utility_data_filename), delimiter=',', lineterminator="\n")
    top_match = []
    best_match = [None, 9999999999]

    origin_address = str(coord[0]) + "," + str(coord[1])

    for asset in utility_data:
        if asset != "" and utility_name_map[utility_type] in asset[3].lower():
            destination_address = asset[12].strip("(").strip(")")

            lat_diff = abs(float(destination_address.split(", ")[0])-float(coord[1]))
            lng_diff = abs(float(destination_address.split(", ")[1])-float(coord[0]))
            trig_distance = (lat_diff**2 + lng_diff**2)**0.5

            FoundAsset = FoundObject(asset, trig_distance, destination_address)

            replaced_object = None
            for match in range(len(top_match)):
                if top_match[match].distance > FoundAsset.distance:
                    replaced_object = top_match[match]
                    top_match[match] = FoundAsset
                elif replaced_object != None:
                    swap_slot = top_match[match]
                    top_match[match] = replaced_object
                    replaced_object = swap_slot

            if len(top_match) <= 1:
                if replaced_object == None:
                    top_match.append(FoundAsset)
                else:
                    top_match.append(replaced_object)

    for match in top_match:
        result = gmaps.distance_matrix(origin_address, match.address, mode="walking")
        distance = result["rows"][0]["elements"][0]["distance"]["value"]

        if float(distance) < float(best_match[1]):
            best_match[1] = distance
            best_match[0] = [match.name, match.location, match.address]

    return best_match


def get_direction(initial, destination):

    directions = gmaps.directions(str(initial[0])+","+str(initial[1]), destination, mode="walking")[0]['legs'][0]['steps'][0]

    end_lat = directions['end_location']['lat']
    end_lng = directions['end_location']['lng']
    start_lat = directions['start_location']['lat']
    start_lng = directions['start_location']['lng']

    end = (end_lat, end_lng)
    start = (start_lat, start_lng)

    def calculate_initial_compass_bearing(pointA, pointB):
        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])
     
        diffLong = math.radians(pointB[1] - pointA[1])
     
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))
     
        initial_bearing = math.atan2(x, y)

        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
     
        return compass_bearing

    final_bearing = calculate_initial_compass_bearing(start, end)
    return final_bearing




