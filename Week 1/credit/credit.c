// Jorge Daniel Gómez Quintana "Credit"
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long num = get_long("Number: ");
    if (num <= 0)
    {
        printf("INVALID\n");
        return 0;
    }
    // Count the number of digits
    int length = 0;
    long temp = num;
    while (temp > 0)
    {
        temp /= 10;
        length++;
    }
    // Check valid length
    if (length != 13 && length != 15 && length != 16)
    {
        printf("INVALID\n");
        return 0;
    }
    // Determine first and first two digits
    long first_two = num;
    while (first_two >= 100)
    {
        first_two /= 10;
    }
    int first_digit = first_two / 10;
    // Check card type
    int isAmex = (length == 15 && (first_two == 34 || first_two == 37));
    int isMaster = (length == 16 && (first_two >= 51 && first_two <= 55));
    int isVisa = (length == 13 || (length == 16 && first_digit == 4));

    if (!isAmex && !isMaster && !isVisa)
    {
        printf("INVALID\n");
        return 0;
    }
    // Luhn's Algorithm
    temp = num;
    int sum = 0;
    int multiply = 0;

    while (temp > 0)
    {
        int digit = temp % 10;
        if (multiply)
        {
            digit *= 2;
            sum += (digit / 10) + (digit % 10);
        }
        else
        {
            sum += digit;
        }
        multiply = !multiply;
        temp /= 10;
    }

    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    // Dteremine card type
    if (isAmex)
    {
        printf("AMEX\n");
    }
    else if (isMaster)
    {
        printf("MASTERCARD\n");
    }
    else if (isVisa)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
