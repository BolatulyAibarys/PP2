#Multiple inheritance — это когда один класс наследуется сразу от нескольких классов

class Fly:
    def move(self):
        print("Flying")

class Swim:
    def move_in_water(self):
        print("Swimming")


class Duck(Fly, Swim):
    def speak(self):
        print("Quack")


duck = Duck()
duck.move()
duck.move_in_water()
duck.speak()