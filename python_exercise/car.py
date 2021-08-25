class Car:
    def __init__(self,make,model,year):
        self.make=make
        self.model = model
        self.year = year
        self.odometer_reading=0

    def get_descriptive_name(self):
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def update_odometer(self,mileage):
        #self.odometer_reading=mileage
        
        if mileage>= self.odometer_reading:
            self.odometer_reading =mileage
            
        else:
            print("you can't roll back odometer!")
    
    def increment_odometer(self,miles):
        self.odometer_reading += miles

    def read_odometer(self):
        print(f"this car has {self.odometer_reading} miles on it.")

'''
my_car=Car('audi','a4',2019)
print(my_car.get_descriptive_name())
my_car.update_odometer(35000)
my_car.read_odometer()

my_car.increment_odometer(10000)
my_car.read_odometer()

'''

class Bettery:
    def __init__(self,battery_size=75):
        self.battery_size=battery_size
    
    def descripe_bettery(self):
        print(f"this car has a {self.battery_size}-kwh battery.")


class ElectricCar(Car):
    def __init__(self,make,model,year):
        super().__init__(make,model,year)
        self.bettery = Bettery

my_tesla=ElectricCar('tesla','models',2019)
print(my_tesla.get_descriptive_name())















