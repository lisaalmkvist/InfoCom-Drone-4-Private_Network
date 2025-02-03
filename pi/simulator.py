import math
import requests
import argparse

def getMovement(src, dst):
    speed = 0.00001
    dst_x, dst_y = dst
    x, y = src
    direction = math.sqrt((dst_x - x)**2 + (dst_y - y)**2)
    longitude_move = speed * ((dst_x - x) / direction )
    latitude_move = speed * ((dst_y - y) / direction )
    return longitude_move, latitude_move

def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la        
    return (x, y)

def run(current_coords, from_coords, to_coords, SERVER_URL):
    drone_coords = current_coords
    d_long, d_la =  getMovement(drone_coords, from_coords)
    while ((from_coords[0] - drone_coords[0])**2 + (from_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                            'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
    d_long, d_la =  getMovement(drone_coords, to_coords)
    while ((to_coords[0] - drone_coords[0])**2 + (to_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                            'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
   
if __name__ == "__main__":
    SERVER_URL = "http://192.168.1.50:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords, from_coords, to_coords)
    run(current_coords, from_coords, to_coords, SERVER_URL)
