# from itertools import cycle

# def next_player(dictionary_of_seats, start_key):
#     keys_iterator = cycle(dictionary_of_seats.keys())
#     # If a start key is provided, advance the iterator to that key
#     if start_key is not None:
#         while next(keys_iterator) != start_key:
#             pass
#     # Loop for the maximum amount of players
#     for bla in range(0, 10):
#         current_key = next(keys_iterator)
#         print('check {current_key}')
#     # Access the corresponding value in the dictionary
#         current_value = dictionary_of_seats[current_key]
#     # Check if the value is not None
#         if current_value is not None:
#             print('de volgende speler is {current_key}')
#             return current_key

class human():
    def __init__(self, name):
        self.name = name
        print(f"{self.name} is a human according to the parent class")
        self.oren = 2

    def itch(self):
        print(f'{self.name} scratches')

class student(human):
    pass

object = student("Jaap")
object.itch()
print(f"{object.name} has {object.oren} ears")

"""
#AttributeError: 'student' object has no attribute 'name': object is niet nodig?

class student2(human):
    def __init__(self):
        self.oren = 3

object = student2("object")
object.itch()
print(object.oren)
"""


# hier mist ie dus omdat hij student mist?

# class student2(human):
#     def __init__(self):
#         self.oren = 3

# object = student2()
# object.itch()
# print(object.oren)

# TypeError: student2.__init__() takes 1 positional argument but 2 were given

# class student2(human):
#     def __init__(self):
#         self.oren = 3

# object = student2("object")
# object.itch()
# print(object.oren)

# adding name:
# AttributeError: 'student2' object has no attribute 'name'

# class student2(human):
#     def __init__(self, name):
#         self.oren = 3

# frits = student2("Frits")
# frits.itch()
# print(frits.oren)

# this works, because ... it cannot use the init from the parent to refer to it's own functionalities in this class without the super()?
# it doesn't however replace the number of ears.

# class student2(human):
#     def __init__(self, name):
#         self.oren = 3
#         super().__init__(name)

# object = student2("object")
# object.itch()
# print(object.oren)

# this does, so you need to do that after you initialize the child class. Better to not define if you want to change it I guess.

class student2(human):
    def __init__(self, name):
        self.oren = 3
        super().__init__(name)
        self.oren = 4
    
    def itch(self):
        print(f"{self.name} is a student, so he scratches some more")

object = student2("Kees")
object.itch()
print(f"{object.name} has {object.oren} ears")

test = ['a', 'b', 'a']