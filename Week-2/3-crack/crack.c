#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <string.h>
#include <ctype.h>

bool brute(int l, string hash_salt, string salt);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;    
    }
    string salt_hash = argv[1];
    int salt_hash_length = strlen(salt_hash);
    char salt[2];
    char hash[salt_hash_length];
    // Retrieve salt
    int i = 0;
    while (salt_hash[i] != '\0' && i < 2)
    {
        salt[i] = salt_hash[i];
        i++;
    }
    // Retrieve hash
    int j = 0;
    while (salt_hash[i] != '\0')
    {
        hash[j++] = salt_hash[i++]; 
    }
    // Let's crack it :)
    if (brute(1, salt_hash, salt) ||
        brute(2, salt_hash, salt) ||
        brute(3, salt_hash, salt) ||
        brute(4, salt_hash, salt) ||
        brute(5, salt_hash, salt))
    {
        return 0;
    }
}

bool brute(int l, string salt_hash, string salt)
{
    // Initialize brute force array
    char a[l];
    for (int i = 0; i < l; i++)
    {
        a[i] = 'A';
    }
    // Increment pointer
    int p = l - 1;
    // Stop pointer
    int stop = 0;
    // Brute force cycle
    while (true)
    {
		// Ensure alphabetical char
        if (!isalpha(a[p]))
        {
            a[p]++;
            continue;    
        }
        // Check hash equality
        char chk[l + 1];
        for (int i = 0; i < l; i++)
        {
            chk[i] = a[i];
        }
        chk[l] = '\0';
        string s_crack = crypt(chk, salt);
        int eq = strcmp(s_crack, salt_hash);
        if (eq == 0)
        {
            // Password cracked successfully
            printf("%s\n", chk);
            return true;
        }
        // Stop condition
        if (a[p] == 'z' && p == stop)
        {
            p++;
            stop++;
            if (stop == l)
            {
                return false;
            }
        }
        // Clear counter and move pointer left
        if (a[p] == 'z')
        {
            a[p] = 'A';
            p--;
        } 
        else if (p < l - 1)    
        {
            // Move pointer right 
            p++;
            continue;
        }
        // Increment counter
        a[p]++;
    }
}