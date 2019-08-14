class Car:

    def __init__(self,):
        self.xpos = 100
        self.ypos = 50
        self.angle = 90
        self.speed = 0
        self.odometer = 0
        self.time = 0
        self.speed_inc = 2

    def say_state(self):
        print("Current speed is {} kph".format(self.speed))

    def accelerate(self):
        self.speed += self.speed_inc

    def brake(self):
        if self.speed < self.speed_inc:
            self.speed = 0
        else:
            self.speed -= self.speed_inc

    def step(self):
        self.odometer += self.speed
        self.time += 1
        self.ypos += self.speed

    def average_speed(self):
        if self.time != 0:
            return self.odometer / self.time
        else:
            pass

if __name__ == "__main__":
    my_car = Car()
    print("This is car")