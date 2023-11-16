import truck
import csv
import package
import hashTables as ht
from datetime import datetime, timedelta, time

#import and clean the data
with open('packageFile.csv', mode='r') as file:
    package_file = csv.reader(file)
    package_file_list = list(package_file)

package_data = []

package_file_list_data = package_file_list[1:]

for i in range(len(package_file_list_data)):
    row = package_file_list_data[i]
    sliced_elements = [row[i] for i in [0, 1, 2, 4, 5, 6]]
    package_data.append(sliced_elements)

#create package hash table
package_ht = ht.HashTable()
for i in range(len(package_data)):
    id = package_data[i][0]
    address = package_data[i][1]
    city = package_data[i][2]
    zip_code = package_data[i][3]
    package_weight = package_data[i][5]
    deadline = package_data[i][4]
    _package = package.Package(id, address, city, zip_code, deadline, package_weight)
    package_ht.insert(id, _package)


# calclate distances
with open('distanceTable.csv', mode='r') as file:
    distance_table = csv.reader(file)
    distance_table_list=list(distance_table)


#find index of addresses
def index_of_address(address):
    row_num = 0
    for i in distance_table_list:
        if i[0] == address:
            return row_num
        row_num += 1
    return -1

#get the distance between two addresses
def get_distance(address1, address2):
    index1 = index_of_address(address1)
    index2 = index_of_address(address2)
    if index1 == -1 or index2 == -1:
        print('bad address', address1, address2 , '\n')
        exit()
    if index1 > index2:
        return float(distance_table_list[index1][index2+1])
    else:
        return float(distance_table_list[index2][index1+1])
    
#get a list of packages for a certain address   
def get_list_of_packages(address):
    package_list = []
    for i in range(1, 41):
        p = package_ht.lookup(i)
        if p.address == address:
            package_list.append(p)
    return package_list
        

#find the nearest neighbors for trucks
def nearest_neighbors(locations, truck):
    distance_traveled = 0
    num_locations = len(locations)
    current_location = 'HUB'
    route = [current_location]
    
    initial_time = truck.departure_time
    minutes_to_destination = 0.0
    current_time = (initial_time+timedelta(minutes=minutes_to_destination))
    
    locations_visited = {current_location : [True, current_time, distance_traveled]}
 
    while len(route) < num_locations+1:
        
        closest_distance = 1000
        closest_location = None
        
        for new_location in locations:
            distance_from_current = get_distance(current_location, new_location)
            if distance_from_current < closest_distance:
                closest_location = new_location
                closest_distance = distance_from_current
                
        current_location = closest_location
        locations.remove(current_location)
                
        truck.distance_traveled += closest_distance
        route.append([current_location])
        
        minutes_to_destination = (closest_distance/18.0)*60.0
        current_time = (current_time+timedelta(minutes=minutes_to_destination))
        
        package_list = get_list_of_packages(current_location)
        
        for i in package_list:
            if truck.id == 1: 
                if int(i.id) in load1:
                    i.delivery_time = current_time
                    i.truck_number = truck.id
            if truck.id == 2:
                if int(i.id) in load2:
                    i.delivery_time = current_time
                    i.truck_number = truck.id
            if truck.id == 3:
                if int(i.id) in load3:
                    i.delivery_time = current_time
                    i.truck_number = truck.id



#load up trucks with packages
load1 = [1, 2, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 39, 40]
load2 = [3, 5, 6, 18, 25, 26, 36, 37, 38]
load3 = [4, 7, 8, 9, 10, 11, 12, 17, 22, 23, 24, 27, 28, 32, 33, 35]

truck1=truck.Truck(1, load1, timedelta(hours = 8))
truck2=truck.Truck(2, load2, timedelta(hours = 9, minutes = 5))
truck3=truck.Truck(3, load3, timedelta(hours = 10, minutes = 30))


#handle address change
package_ht.lookup(9).address='410 S State St'
package_ht.lookup(9).city='Salt Lake City'
package_ht.lookup(9).state='UT'
package_ht.lookup(9).zip_code='84111'


#convert package ids to locations and calculate the optimal path for the trucks
package_locations_list = []
truck_list = [truck1, truck2, truck3]
for truck in truck_list:
    for i in truck.packages:
        package_ht.lookup(i).departure_time = truck.departure_time
        package_location = package_ht.lookup(i).address
        package_locations_list.append(package_location)
    truck_results = nearest_neighbors(package_locations_list, truck)


#user interface
while True:
    print("\nTotal Mileage for All Trucks: ", round(truck1.distance_traveled+truck2.distance_traveled+truck3.distance_traveled, 2))
    user_input= int(input(("\nChoose:\n1 - For All Packages\n2 - To Search for a Package ID\n3 - To See a Snapeshot of Time\n4 - To Exit:\n\n")))
    
    # option 1
    if user_input == 1:
        for i in range(1,41):
            print(package_ht.lookup(i))
        
    # option 2
    if user_input == 2:
        package_id = int(input("Enter Package ID: "))
        print(package_ht.lookup(package_id))

    # option 3
    if user_input == 3:
        user_time = input("Enter a Time [hh:mm]: ")
        user_time_value = user_time.split(":")
        user_time_dt = timedelta(hours=int(user_time_value[0]), minutes=int(user_time_value[1]))
        package_id = int(input("Enter Package ID (Or 0 for All Packages): "))
        print("\n")
        if package_id == 0:
            start = 1
            end = 41
        else:
            start = package_id
            end = start+1
        for i in range(start, end):
            p=package_ht.lookup(i)
            status = "At Hub"
            if user_time_dt > p.delivery_time:
                status = "Delivered"
            elif user_time_dt < p.delivery_time and user_time_dt > p.departure_time:
                status = "En Route"
            p.print_status(status, user_time_dt)
        
    # option 4
    if user_input == 4:
        exit()
