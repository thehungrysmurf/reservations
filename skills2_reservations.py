"""
Reservation finder

Along with this file, you'll find two files named units.csv and reservations.csv with fields in the following format

units.csv
location_id, unit_size

reservations.csv
location_id, reservation_start_date, reservation_end_date

You will write a simple application that manages a reservation system. It will have two commands, 'available' and 'reserve' with the following behaviors:

available <date> <number of occupants> <length of stay>
This will print all available units that match the criteria. Any unit with capacity equal or greater to the number of occupants will be printed out.

Example:
SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available

reserve <unit number> <start date> <length of stay>
This creates a record in your reservations that indicates the unit has been reserved. It will print a message indicating its success.

A reservation that ends on any given day may be rebooked for the same evening, ie:
    
    If a reservation ends on 10/10/2013, a different reservation may be made starting on 10/10/2013 as well.

Example:
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights

Reserving a unit must make the unit available for later reservations. Here's a sample session:

SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights
SeaBnb> available 10/10/2013 2 4
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Unit 10 is unavailable during those dates
SeaBnb> quit

Notes:
Start first by writing the functions to read in the csv file. These have been stubbed for you. Then write the availability function, then reservation. Test your program at each step (it may be beneficial to write tests in a separate file.) Use the 'reservations' variable as your database. Store all the reservations in there, including the ones from the new ones you will create.

The datetime and timedelta classes will be immensely helpful here, as will the strptime function.
"""

import sys
import datetime

def parse_one_record(line):
    """Take a line from reservations.csv and return a dictionary representing that record. (hint: use the datetime type when parsing the start and end date columns)"""
    d = {}
    line_element = []
    start_date = []
    end_date = []
    line_element = line.split(",")
    d["room"] = line_element[0].strip()
    start_date=line_element[1].strip().split("/")
    d["start_date"] = datetime.datetime(int(start_date[2]), int(start_date[0]), int(start_date[1]))
    end_date = line_element[1].strip().split("/")
    d["end_date"] = datetime.datetime(int(end_date[2]), int(end_date[0]), int(end_date[1]))
    return d

def read_units():
    """Read in the file units.csv and returns a list of all known units."""
    units = []
    line = open("units.csv").readlines()
    for item in line:
        item=item.split(',')
        units.append({"room": item[0].strip(), "capacity": item[1].strip()})
    return units

def read_existing_reservations():
    """Reads in the file reservations.csv and returns a list of reservations."""
    reservations = []
    list_of_lines = open("reservations.csv").readlines()
    for each in list_of_lines:
        reservations.append(parse_one_record(each.strip()))
    return reservations

def overlap(start1, end1, start2, end2):
    if start2 > end1 or start1 >= end2:
        return False
    return True

def available(units, reservations, start_date, occupants, stay_length):
    unavailable = []
    unit_id = []
    occupied = 0
    start_date_list = start_date.split("/")
    start_date_formatted = datetime.datetime(int(start_date_list[2]), int(start_date_list[0]), int(start_date_list[1]))
    end_date = start_date_formatted + datetime.timedelta(days=int(stay_length))
    for r in reservations:
        if overlap(start_date_formatted, end_date, r["start_date"], r["end_date"]):
            unavailable.append(r["room"])
    for room in units:
        if room["room"] not in unavailable:
            unit_id.append({"id": room["room"], "capacity": room["capacity"]})
            occupied += int(room["capacity"])
            if occupied >= int(occupants):
                break  
    for i in range(len(unit_id)):
        print "Unit %s is available, with capacity %s." %(unit_id[i]["id"], unit_id[i]["capacity"])
    return unit_id

    """
    while(occupied < int(occupants)):
        for j in range(len(units)-1):
            for i in range(len(reservations)-1):
                if reservations[i]["room"] == units[j]["room"]:
                    if not overlap(start_date_formatted, end_date, reservations[i]["start_date"],reservations[i]["end_date"]):
                        unit_id.append({"free_room": units[j]["room"], "room_capacity": units[j]["capacity"]})
                        if units[j]["capacity"]>=int(occupants):
                            occupied += int(occupants)
                            print "The room is on the reservations list, there's no overlap, room capacity >= occupants. Occupied: ", occupied
                            break
                        else:
                            occupied += units[j]["capacity"]
                            print "The room is on the reservations list, there's no overlap, but room capacity< occupants. Occupied: ", occupied
                else:
                    unit_id.append({"free_room": units[j]["room"], "room_capacity": units[j]["capacity"]})
                    if units[j]["capacity"] >= int(occupants):
                        occupied += int(occupants)
                        print "The room is NOT on the reservations list, room capacity >= occupants. Occupied: ", occupied
                        break
                    else:
                        occupied += units[j]["capacity"]
                        print "The room is NOT on the reservations list, but room capacity < occupants. Occupied: ", occupied
    for item in unit_id:
        print "Unit %s is available, with capacity of %s." %(item["free_room"], item["room_capacity"])
    """

def reserve(units, reservations, unit_id, start_date, stay_length):
    #if available(units, reservations, unit_id)
    print "Successfully reserved"

def main():
    line = []
    units = read_units()
    reservations = read_existing_reservations()

    while True:
        command = raw_input("SeaBnb> ")
        cmd = command.split()
        if cmd[0] == "available":
            # look up python variable arguments for explanation of the *
            available(units, reservations, *cmd[1:])
        elif cmd[0] == "reserve":
            reserve(units, reservations, *cmd[1:])
        elif cmd[0] == "quit":
            sys.exit(0)
        else:
            print "Unknown command"

if __name__ == "__main__":
    main()