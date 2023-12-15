from collections import deque

# def rotate_list(lst):
#     # Convert the list to a deque
#     rotated_lst = deque(lst)

#     # Rotate the deque to the right by one position
#     rotated_lst.rotate(-1)

#     # Convert the deque back to a list
#     result = list(rotated_lst)

#     return result

# # Example usage
# original_list = [1, 2, 3, 4]
# result_list = rotate_list(original_list)

# print(result_list)

# print(deque(['a', 'b', 'c']))
# print(deque(['a', 'b', 'c']).rotate())
# list2 = deque(['a', 'b', 'c']).rotate(1)
# print(list2)
# list2.rotate()
# print(list2)
# list2.rotate(9)

# how fast or slow is a for loop really?

# # use Id's to track
# testlist = [1,2]
# print('oude list: ', id(testlist))

# for i in range(len(testlist)):
#     # print('id_inhoud: ', id(i), testlist)
#     testlist.append(i+5)
#     print('nieuwe list: ', id(testlist), testlist)

# print('new list', id(testlist), testlist)

test_int = 1

print('test_int1: ', id(test_int), test_int)

def change_int(the_input):
    print('the_input: ', id(the_input), the_input)
    the_input +=1
    print('the_input: ', id(the_input), the_input)
    return the_input
    
the_output = change_int(test_int)

print('test_int2: ', id(test_int), test_int)
print('the_output: ', id(the_output), the_output)

class Testclass:
    def __init___(self):
        self.test_int2 = 1
    
    def change_int_method(self):
        print('the_input_in_method: ', id(self), self)
        self +=1
        print('the_input_in_method: ', id(self), self)

# make a second one for different print statements
    def change_int_method_2(self, the_input_is_a_class):
        print('the_class_input_in_method: ', id(the_input_is_a_class), the_input_is_a_class)
        the_input_is_a_class +=1
        print('the_class_input_in_method2: ', id(the_input_is_a_class), the_input_is_a_class)

print('running the method on a variable', id(Testclass.change_int_method(test_int)), Testclass.change_int_method(test_int))
saving_the_method = Testclass.change_int_method(test_int)
print('running the saved method', id(saving_the_method), saving_the_method)

the_class_init = Testclass()

print('running the method on a class attribute', id(Testclass.change_int_method(the_class_init.test_int2)), Testclass.change_int_method(the_class_init.test_int2))
saving_the_method = Testclass.change_int_method(the_class_init.test_int2)
