#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int shift(char c);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    // Validate key
    string s = argv[1];
    int i = 0;
    char c = s[i];  
    while (c != '\0')
    {
        if (!isalpha(c))
        {
            printf("Usage: ./vigenere keyword\n");
            return 1;
        }
        c = s[++i];
    }
    int keylen = strlen(s);
    int k = 0;
    // Ask user for a plain text
    string plain = get_string("plaintext: ");
    // Encrypt plain text using user key
    c = plain[0];
    i = 0;
    printf("ciphertext: ");
    while (c != '\0')
    {
        // Loop key
        if (k >= keylen)
        {
            k = 0;
        }
        int key = shift(s[k]);
        // Cypher
        char ck = c;
        if (c >= 'a' && c <= 'z')
        {
            // Check lower case
            ck = (c + key) > 'z' ? 'a' + (c + key - 1) - 'z' : (c + key);
            k++;
        } 
        else if (c >= 'A' && c <= 'Z')
        {
            // Check upper case
            ck = (c + key) > 'Z' ? 'A' + (c + key - 1) - 'Z' : (c + key);
            k++;
        } 
        printf("%c", ck);
        // Pick next char
        c = plain[++i];
    }
    printf("\n");
}

// Convert character into the correct shift value
int shift(char c)
{
    if (c >= 'a' && c <= 'z')
    {
        // Check lower case
        return c - 'a';
    } 
    else if (c >= 'A' && c <= 'Z')
    {
        // Check upper case
        return c - 'A';
    }
    return c;
}
