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

# wierd, python doesn't update
testlist = [1,2,3,4]
for i in range(len(testlist)):
    print(i)
    testlist.append(i+5)
    print(testlist)