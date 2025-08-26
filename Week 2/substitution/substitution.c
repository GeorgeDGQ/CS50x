// Jorge Daniel Gómez Quintana "Substitution"
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // validate command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    int length = strlen(key);

    // Validate key length
    if (length != 26)
    {
        printf("key must contain 26 characters.\n");
        return 1;
    }

    int seen[26] = {0};

    for (int i = 0; i < length; i++)
    {
        char c = key[i];

        if (!isalpha(c))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }

        // Convert uppercase
        char upper_c = toupper(c);
        int index = upper_c - 'A';

        if (seen[index])
        {
            printf("Key must not contain duplicate letters.\n");
            return 1;
        }

        seen[index] = 1;
    }

    // Get plaintext input
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    // Encrypt each character
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];

        if (isupper(c))
        {
            int index = c - 'A';
            printf("%c", toupper(key[index]));
        }
        else if (islower(c))
        {
            int index = c - 'a';
            printf("%c", tolower(key[index]));
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
    return 0;
}
