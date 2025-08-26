# Jorge Daniel Gómez Quintana "Sentimental Mario More"

while True:
    try:
        height = int(input("What is the height of the pyramid?"))
        if 1 <= height <= 8:
            break
        else:
            print("Repeat: Height must be between 1 and 8, inclusive.")
    except ValueError:
        print("Please enter a valid integer between 1 and 8.")

for i in range(1, height + 1):
    # Print leading spaces
    print(" " * (height - i), end="")

    # Print left pyramid
    print("#" * i, end="")

    # Print gap
    print("  ", end="")

    # Print right pyramid
    print("#" * i)
