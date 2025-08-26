# Jorge Daniel Gómez Quintana "Sentimental credit"

def main():
    # Get input and validate it's a positive integer
    try:
        num = int(input("Number: "))
        if num <= 0:
            print("INVALID")
            return
    except ValueError:
        print("INVALID")
        return

    # Count digits
    length = 0
    temp = num
    while temp > 0:
        temp //= 10
        length += 1

    # Validate length
    if length not in [13, 15, 16]:
        print("INVALID")
        return

    # Get first two digits
    first_two = num
    while first_two >= 100:
        first_two //= 10
    first_digit = first_two // 10

    # Check card types
    isAmex = (length == 15) and (first_two in [34, 37])
    isMaster = (length == 16) and (51 <= first_two <= 55)
    isVisa = (first_digit == 4) and (length in [13, 16])

    # Validate card type
    if not (isAmex or isMaster or isVisa):
        print("INVALID")
        return

    # Luhn's Algorithm
    temp = num
    total = 0
    alternate = False

    while temp > 0:
        digit = temp % 10
        if alternate:
            digit *= 2
            # Add digits of products
            total += digit // 10 + digit % 10
        else:
            total += digit

        alternate = not alternate
        temp //= 10

    # Validate checksum
    if total % 10 != 0:
        print("INVALID")
        return

    # Output card type
    if isAmex:
        print("AMEX")
    elif isMaster:
        print("MASTERCARD")
    elif isVisa:
        print("VISA")


if __name__ == "__main__":
    main()
