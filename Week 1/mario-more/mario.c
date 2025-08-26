// Jorge Daniel Gómez Quintana "Mario"
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, i, j;
    // Prompt height
    do
    {
        printf("What is the height of the pyramid ");
        height = get_int("What is the height of the pyramid ");

        if (height <= 0)
        {
            printf("Repeat: Height must be a positive number\n");
        }
    }
    while (height <= 0);

    for (i = 1; i <= height; i++)
    {
        for (j = 0; j < height - i; j++)
        {
            printf(" ");
        }
        // Left pyramid
        for (j = 0; j < i; j++)
        {
            printf("#");
        }
        // Gap between
        printf("  ");
        // Right pyramid
        for (j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

    return 0;
}
