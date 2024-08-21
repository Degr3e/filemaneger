# try: 
#     n = int(input(""))
# except ValueError as e:
#     print("вводить надо было число")
try:
    v = int(input("enter number 1st: "))
    n = int(input("enter number 2nd: "))
    c = v / n
except ZeroDivisionError as e:
    print("На ноль делить нельзя")
except ValueError as e:
    print("вводить надо было число")