# TODO
n = -1
while n < 0:
    n = int(input("Input card number: "))

digit = len(str(n))

if digit not in [13, 15, 16]:
    print("INVALID")
else:
    number = [int(x) for x in str(n)]
    sum_ = sum(number[-1::-2] + [sum(divmod(2 * d, 10)) for d in number[-2::-2]])
    if sum_ % 10 != 0:
        print("INVALID")
    elif digit in [13, 16] and number[0] == 4:
        print("VISA")
    elif digit == 16 and number[0] == 5 and number[1] in [1, 2, 3, 4, 5]:
        print("MASTERCARD")
    elif digit == 15 and number[0] == 3 and number[1] in [4, 7]:
        print("AMEX")
    else:
        print("INVALID")
