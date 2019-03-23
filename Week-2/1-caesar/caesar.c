#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    //validate key
    int i = 0;
    string s = argv[1];
    char c = s[i];  
    while (c != '\0')
    {
        if (!isdigit(c))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        c = s[++i];
    }
    //convert key to int
    int key = atoi(s) % 26;
    //check full shift case
    if (key > 26)
    {
        key = key % 26;
    }
    //ask user for a plain text
    string plain = get_string("plaintext: ");
    //encrypt plain text using user key
    c = plain[0];
    i = 0;
    printf("ciphertext: ");
    while (c != '\0')
    {
        //printf("%c\n", c);
        char ck = c;
        if (c >= 'a' && c <= 'z')
        {
            //check lower case
            ck = (c + key) > 'z' ? 'a' + (c + key - 1) - 'z' : (c + key);
        } 
        else if (c >= 'A' && c <= 'Z')
        {
            //check upper case
            ck = (c + key) > 'Z' ? 'A' + (c + key - 1) - 'Z' : (c + key);
        } 
        printf("%c", ck);
        //pick next char
        c = plain[++i];
    }
    printf("\n");
}