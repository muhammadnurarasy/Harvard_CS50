# TODO
while True:
    try:
        n = input("Height of the pyramid: ")
        n = int(n)
        if 0 < n <= 8:
            break
        else:
            print("Height must be a positive integer between 1 and 8.")
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

for i in range(n):
    print(" " * (n - i - 1) + "#" * (i + 1) + "  " + "#" * (i + 1))

