#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/stat.h>
#include <unistd.h>

// declare BYTE
typedef uint8_t  BYTE;

// declare contains function
int contains(BYTE val, int arrsize, BYTE arr[]);

int main(int argc, char *argv[])
{
    // ensure right usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // open input file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    // get file size
    fseek(file, 0L, SEEK_END);
    int file_size = ftell(file);
    fseek(file, 0L, SEEK_SET);

    // array of first three JPEG bytes
    BYTE jpeg_start[] = {0xff, 0xd8};

    // array of one of the possible 4th JPEG byte
    BYTE byte4[] = {0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef};

    // first bytes counter
    int fc = 0;

    //image counter
    int ic = 0;

    // file pointer for an image
    FILE *image;

    // flag which indicates that image is being recorded
    int flag = 0;

    // iterate bytes in raw file  search for image
    for (int i = 0; i < file_size; i += 512)
    {
        // temporary storage
        BYTE bytes[512];

        // read bytes
        fread(&bytes, 512, 1, file);

        if (bytes[0] == 0xff &&
            bytes[1] == 0xd8 &&
            bytes[2] == 0xff &&
            contains(bytes[3], sizeof(byte4), byte4) == 1)
        {
            // stop write image if new image was found
            if (flag == 1)
            {
                fclose(image);
            }

            // Image was found! Create image name
            char filename[8];
            sprintf(filename, "%03i.jpg", ic++);
            // Open file pointer
            image = fopen(filename, "w");

            if (flag == 0)
            {
                flag = 1;
            }

        }

        // write bytes to image
        if (flag == 1)
        {
            fwrite(&bytes, 512, 1, image);
        }

    }

    // close file pointer
    fclose(file);
}

// function determines if byte is in array
int contains(BYTE val, int arrsize, BYTE arr[])
{
    for (int i = 0; i < arrsize / sizeof(BYTE); i++)
    {
        if (arr[i] == val)
        {
            return 1;
        }
    }
    return 0;
}