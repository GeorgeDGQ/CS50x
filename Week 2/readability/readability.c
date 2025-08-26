// Jorge Daniel Gómez Quintana "Readability"
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Prompt user for text
    string text = get_string("Text: ");

    int letters = 0;
    int spaces = 0;
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        else if (text[i] == ' ')
        {
            spaces++;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    // Calculate word count
    int words = (strlen(text) == 0) ? 0 : spaces + 1;

    float L = 0.0;
    float S = 0.0;
    if (words > 0)
    {
        L = (float) letters / words * 100;
        S = (float) sentences / words * 100;
    }

    // Coleman-Liau Index
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = (int) round(index);

    // Determine grade level
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", grade);
    }

    return 0;
}
