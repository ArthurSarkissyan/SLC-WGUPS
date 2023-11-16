#create truck class
class Truck:
    def __init__(self, id, package_list=[], departure_time = None):
        self.id = id
        self.packages = package_list
        self.departure_time = departure_time
        self.distance_traveled = 0.0