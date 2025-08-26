// Jorge Daniel Gómez Quintana "Speller"
// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table (prime number for better distribution)
const unsigned int N = 10007;

// Hash table
node *table[N];

// Global variable to store number of words loaded
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    char temp[LENGTH + 1];
    int i = 0;
    for (; word[i] != '\0'; i++)
    {
        temp[i] = tolower((unsigned char) word[i]);
    }
    temp[i] = '\0';

    unsigned int index = hash(temp);
    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
    {
        if (strcmp(temp, cursor->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int h = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        h = (h * 31 + (unsigned char) tolower(word[i])) % N;
    }
    return h;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(file);
            return false;
        }
        strcpy(n->word, word);
        unsigned int index = hash(word);
        n->next = table[index];
        table[index] = n;
        word_count++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        table[i] = NULL;
    }
    return true;
}
