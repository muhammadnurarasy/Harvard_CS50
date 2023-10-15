// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    bool hasUpper = false;
    bool hasLower = false;
    bool hasNumber = false;
    bool hasSymbol = false;

    for (int i = 0; password[i] != '\0'; i++)
    {
        if (isupper(password[i]))
        {
            hasUpper = true;
        }
        if (islower(password[i]))
        {
            hasLower = true;
        }
        if (isdigit(password[i]))
        {
            hasNumber = true;
        }
        if (ispunct(password[i]))
        {
            hasSymbol = true;
        }
    }
    if (hasUpper && hasLower && hasNumber && hasSymbol)
    {
        return true;
    }
    else
    {
        return false;
    }
}
