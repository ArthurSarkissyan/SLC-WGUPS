#create HashTable class
class HashTable:
    def __init__(self):
        self.size = 10
        self.table = [None] * self.size
    
    def get_index(self, key):
        return int(key) % self.size
    
    def insert(self, key, value):
        key_value = [key, value]
        index = self.get_index(key)
        if self.table[index] is None:
            self.table[index] = [key_value]
        else:
            found = False
            for pair in self.table[index]:
                if pair[0] == key:
                    pair[1] = value
                    found = True
                    break
            if not found:
                self.table[index].append(key_value)
    
    def lookup(self, key):
        index = self.get_index(key)
        if self.table[index] is not None:
            for package_details in self.table[index]:
                if int(package_details[0]) == key:
                    return package_details[1]
        return None