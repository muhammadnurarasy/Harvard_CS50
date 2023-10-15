#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int is_valid_key(string key);

int main(int argc, string argv[])
{
    // Check if the correct number of arguments is given
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Check if the key is valid
    string key = argv[1];
    if (!is_valid_key(key))
    {
        return 1;
    }

    // Ask for plain text
    string plaintext = get_string("plaintext: ");

    // Encrypt the plaintext
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                printf("%c", toupper(key[plaintext[i] - 'A']));
            }
            else
            {
                printf("%c", tolower(key[plaintext[i] - 'a']));
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
    return 0;
}

// Function to check if the key is valid
int is_valid_key(string key)
{
    int letters[26] = {0};

    // Check length
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 0;
    }

    // Check characters
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 0;
        }

        int index = toupper(key[i]) - 'A';
        if (letters[index] != 0)
        {
            printf("Key must not contain repeated characters.\n");
            return 0;
        }

        letters[index] = 1;
    }
    return 1;
}
