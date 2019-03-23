#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // Read change owed
    float dollars;
    do 
    {
        dollars = get_float("Change owed: ");
    } 
    while (dollars <= 0);
    // Convert to cents
    int cents = round(dollars * 100);
    // Add quarter coin count
    int coins = 0;
    while (cents >= 25)
    {
        cents -= 25;
        coins++;
    }
    // Add dime coin count
    while (cents >= 10)
    {
        cents -= 10;
        coins++;
    }
    // Add nickel coin count
    while (cents >= 5)
    {
        cents -= 5;
        coins++;
    }
    // Add rest of pennie coin count
    coins += cents;
    printf("%i\n", coins);
}