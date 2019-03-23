#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Read heigh
    int h;
    
    do 
    {
        h = get_int("Height: ");
    } 
    while (h < 1 || h > 8);
    
    // Build pyramide
    for (int i = 0; i < h; i++)
    {
        int j;
        
        // Empty spaces
        for (j = i; j < h - 1; j++)
        {
            printf(" ");  
        }
            
        // Bricks
        for (int k = j; k < h + i; k++)
        {
            printf("#"); 
        }
        
        // Next line 
        printf("\n");
    }
}