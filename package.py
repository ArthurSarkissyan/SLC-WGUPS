from datetime import datetime, timedelta, time

#create package class
class Package:
    def __init__(self, id, address, city, zip_code, deadline, package_weight):
        self.id = id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.package_weight = package_weight
        self.departure_time = None
        self.delivery_status = 'Delivered'
        self.delivery_time = None
        self.truck_number = None
        
    def __str__(self):
        return f"{self.id}, {self.address}, {self.city}, {self.zip_code}, {self.package_weight}, {self.departure_time}, {self.deadline}, {self.delivery_status}, {self.delivery_time}, Truck: {self.truck_number}"

    def print_status(self, status, user_time):
        address = self.address
        delivery_time = ''
        if status == 'Delivered':
            delivery_time = self.delivery_time
        if int(self.id) == 9 and user_time < timedelta(hours=10, minutes=20):
            address = '300 State St'
        return print(f"{self.id}, {address}, {self.city}, {self.zip_code}, {self.package_weight}, {self.departure_time}, {self.deadline}, {status}, {delivery_time}, Truck: {self.truck_number}")
