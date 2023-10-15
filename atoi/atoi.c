#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    int length = strlen(input);

    // Base case: If the string is empty, return 0.
    if (length == 0)
    {
        return 0;
    }

    // Convert the last character to its integer value.
    int lastDigit = input[length - 1] - '0';

    // Create a new string without the last character.
    char shortened[length]; // length includes space for '\0'
    strncpy(shortened, input, length - 1);
    shortened[length - 1] = '\0';

    // Recursively call convert with the shortened string and add the value of the last digit.
    return lastDigit + 10 * convert(shortened);
}
