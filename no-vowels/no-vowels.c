// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <stdio.h>
#include <string.h>
#include <cs50.h>

// Replace function
string replace(string input) {
    for (int i = 0; i < strlen(input); i++) {
        switch (input[i]) {
            case 'a':
            case 'A':
                input[i] = '6';
                break;
            case 'e':
            case 'E':
                input[i] = '3';
                break;
            case 'i':
            case 'I':
                input[i] = '1';
                break;
            case 'o':
            case 'O':
                input[i] = '0';
                break;
            case 'u':
            case 'U':
                input[i] = 'u';
                break;
        }
    }
    return input;
}

// Main function
int main(int argc, string argv[]) {
    if (argc != 2) {
        printf("Error: Please provide one argument\n");
        return 1;
    }

    string output = replace(argv[1]);
    printf("%s\n", output);
    return 0;
}

