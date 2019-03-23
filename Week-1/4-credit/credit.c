#include <stdio.h>
#include <cs50.h>
#include <math.h>

int get_digits_count_long(long num);
int get_digits_count_int(int num);
int get_num_end(long num, int digit);

int main(void) 
{
    // Read credit card number
    long num;
    do 
    {
        num = get_long("Number: ");
    }
    while (num < 0);
    int digits = get_digits_count_long(num);
    int sum = 0;
    // Scan digits
    for (int i = 1; i <= digits; i += 1)
    {
        int digit = get_num_end(num, i);
        if (i % 2 == 0)
        {
            // Multiply every other digit by 2
            int product = digit * 2;
            int product_digits = get_digits_count_int(product);
            for (int j = 1; j <= product_digits + 1; j++)
            {
                sum += get_num_end(product, j);
            }
        } 
        else
        {
            // Add the sum to the sum of the digits that weren’t multiplied by 2
            sum += digit; 
        }
    }
    // Check company
    if (sum % 10 == 0)
    {
        int first_digit = floor(num / pow(10, digits - 1));
        // VISA check
        if (first_digit == 4)
        {
            // VISA check for special case
            if (digits == 13 || digits == 16)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            } 
        } 
        else
        {
            int ten = floor(num / pow(10, digits - 2));
            // AMEX check
            if (ten == 34 || ten == 37)
            {
                printf("AMEX\n");
            } 
            // MASTERCARD check
            else if (ten == 51 || ten == 52 || ten == 53 || ten == 54 || ten == 55)
            {
                printf("MASTERCARD\n"); 
            }
            else
            {
                printf("INVALID\n"); 
            }            
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

// Get count of digits in long number
int get_digits_count_long(long num)
{
    if (num == 0) 
    {
        return 0;
    }  
    return floor(log10(num)) + 1;
}

// Get count of digits in int number
int get_digits_count_int(int num)
{
    if (num == 0)
    {
        return 0; 
    }
    return floor(log10(num)) + 1;
}

// Get specified digit from the end of a number
int get_num_end(long num, int digit)
{
    long p = floor(pow(10, digit));
    return floor(num % p) / floor(pow(10, digit - 1));
}