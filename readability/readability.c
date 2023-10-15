#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

int count_letter(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text:");
    float letter = count_letter(text);
    float word = count_words(text);
    float sentence = count_sentences(text);
    float L = (letter / word) * 100;
    float S = (sentence / word) * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    if (round(index) < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (round(index) >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", round(index));
    }
}

int count_letter(string text)
{
    int count = 0;
    for (int x = 0; x < strlen(text); x++)
    {
        if (isalpha(text[x]))
        {
            count ++;
        }
    }
    printf("Letter: %i\n", count);
    return count;
}

int count_words(string text)
{
    int count = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            count ++;
        }
    }
    printf("Words: %i\n", count);
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int y = 0; y < strlen(text); y++)
    {
        if (text[y] == '.' || text[y] == '!' || text[y] == '?')
        {
            count ++;
        }
    }
    printf("Sentence: %i\n", count);
    return count;
}