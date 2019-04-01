// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

void add_padding(int padding, FILE *outptr);

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // Try convert factor to int
    char *f_ptr = NULL;
    long factor = strtol(argv[1], &f_ptr, 10);
    if (*f_ptr != '\0' && factor >= 0)
    {
        printf("n, the resize factor, must be an integer.\n");
        return 1;
    }

    // Check if factor is in range
    if (factor < 0 || factor > 100)
    {
        printf("n, the resize factor, must satisfy 0 < n <= 100.\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine padding of origin imagefor scanlines
    int old_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // save origin width and height
    int old_width = bi.biWidth;
    int old_height = bi.biHeight;

    // change metadata of scaled image
    bi.biWidth *= factor;
    bi.biHeight *= factor;
    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // calculate size
    bi.biSizeImage = (bi.biWidth * sizeof(RGBTRIPLE) + padding) * abs(bi.biHeight);
    bf.bfSize = 54 + bi.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(bf), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(bi), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(old_height); i < biHeight; i++)
    {
        //declare temp buffer for height scaling
        RGBTRIPLE scanline_buffer[bi.biWidth];
        int pos = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < old_width; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write expanded RGB triple to outfile
            for (int k = 0; k < factor; k++)
            {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                scanline_buffer[pos++] = triple;
            }

        }

        // skip over origin padding
        fseek(inptr, old_padding, SEEK_CUR);

        // add scaled padding
        add_padding(padding, outptr);

        // duplicate lines for scaling
        for (int k = 0; k < factor - 1; k++)
        {
            fwrite(&scanline_buffer, sizeof(scanline_buffer), 1, outptr);
            add_padding(padding, outptr);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

void add_padding(int padding, FILE *outptr)
{
    for (int i = 0; i < padding; i++)
    {
        fputc(0x00, outptr);
    }
}