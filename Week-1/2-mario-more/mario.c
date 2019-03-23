#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Read Heigh
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
        // Empty spaces #1
        for (j = i; j < h - 1; j++)
        {
            printf(" ");  
        }
            
        // Bricks #1
        for (int k = j; k < h + i; k++)
        {
            printf("#"); 
        }
        
        // Gap
        printf("  ");
            
        // Bricks #2
        for (int k = j; k < h + i; k++)
        {
            printf("#"); 
        }
        
        // Next line 
        printf("\n");
    }
}