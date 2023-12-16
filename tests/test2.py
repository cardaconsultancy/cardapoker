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

#############


# test_int = 1

# print('test_int1: ', id(test_int), test_int)

# def change_int(the_input):
#     print('the_input: ', id(the_input), the_input)
#     the_input +=1
#     print('the_input: ', id(the_input), the_input)
#     return the_input
    
# the_output = change_int(test_int)

# print('test_dict: DOES NOT CHANGE, same ID, same score ', id(test_int), test_int)
# print('the_output: DOES CHANGE, different ID, different score ', id(the_output), the_output)

# class Testclass:
#     def __init__(self):
#         self.test_dict = 1
    
#     def change_int_method(self):
#         print('the_input_in_method: ', id(self.test_dict), self.test_dict)
#         self.test_int2 +=1
#         print('the_input_in_method: ', id(self.test_int2), self.test_int2)

# the_class_init = Testclass()
# print('original class id: ', id(the_class_init), the_class_init.test_int2)
# print('running the method on a class attribute')
# Testclass.change_int_method(the_class_init)
# print('original class id after running: ', id(the_class_init), the_class_init.test_int2)

# saving_the_method = Testclass.change_int_method(the_class_init)
# print('running the saved method to check', id(saving_the_method), saving_the_method)

# ############ example ######################
# class Testclass:
#     def __init__(self):
#         self.test_dict = {'a':'b'}
    
#     # def change_int_method(self):
#     #     print('the_input_in_method: ', id(self.test_dict), self.test_dict)
#     #     self.test_dict +=1
#     #     print('the_input_in_method: ', id(self.test_dict), self.test_dict)

#     def change_dict(self, score):
#         print('the_input_in_method: ', id(score), score)
#         score['c'] = 'd'
#         print('the_input_in_method: ', id(score), score)

    

# the_class_init = Testclass()
# # print('original class id: ', id(the_class_init), the_class_init.test_dict)
# the_class_copy = the_class_init.test_dict.copy()
# # print('class_copy id: ', id(the_class_copy), the_class_copy.test_dict)
# the_class_var = the_class_init.test_dict
# # print('class_copy id: ', id(the_class_var), the_class_var)
# the_class_copy_var = the_class_var.copy

# print()
# print()

# the_class_init = Testclass()
# print('--- original class id: ', id(the_class_init.test_dict), the_class_init.test_dict, '---')
# print('running the method on a class attribute')
# Testclass.change_dict(the_class_init.test_dict)
# print('original class id after running: ', id(the_class_init.test_dict), the_class_init.test_dict)

# print('--- original class copy id: ', id(the_class_copy), the_class_copy, '---')
# print('running the method on a class attribute')
# Testclass.change_dict(the_class_copy)
# print('original class id after running: ', id(the_class_copy), the_class_copy)

# print('--- original class id: ', id(the_class_var), the_class_var, '---')
# print('running the method on a class attribute')
# Testclass.change_dict2(the_class_var)
# print('original class id after running: ', id(the_class_var), the_class_var)




testlist = [1,2,3]
print(id(testlist), testlist)
def change_testlist(the_list):
    the_list = the_list + [4]
    print(id(testlist), testlist)
change_testlist(testlist)
print(id(testlist), testlist)
testlist.append(4)
print(id(testlist), testlist)
