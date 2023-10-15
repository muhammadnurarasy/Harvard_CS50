#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int n;
    do
    {
        n = get_int("Start size: ");
    }
    while (n < 9);
    // TODO: Prompt for end size
    int m;
    do
    {
        m = get_int("End size: ");
    }
    while (m < n);
    // TODO: Calculate number of years until we reach threshold
    int x = 0;
    int y = 0;
    for (x = 0; n < m; x += 1)
    {
        n = (n + (n / 3)) - (n / 4);
    }
    // TODO: Print number of years
    printf("Years: %i\n", x);
}
