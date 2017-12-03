lists_of_lists = [[1, 2, 3], [4, 5, 6]]
print zip(lists_of_lists)
print [sum(x) for x in zip(*lists_of_lists)]
# -> [5, 7, 9]