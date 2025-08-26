// Jorge Daniel Gómez Quintana
#include <cs50.h>
#include <stdio.h>

int compute_score(char *word);

int main(void)
{
    // Prompt Player 1
    string word1 = get_string("Player 1: ");

    // Prompt Player 2
    string word2 = get_string("Player 2: ");

    // Compute
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Determine Result
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
    return 0;
}

// Function to compute based on Scrabble
int compute_score(string word)
{
    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int score = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        char c = word[i];
        // Convert ot uppercase
        if (c >= 'a' && c <= 'z')
        {
            c = c - 32;
        }
        if (c >= 'A' && c <= 'Z')
        {
            score += points[c - 'A'];
        }
    }
    return score;
}
