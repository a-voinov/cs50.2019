# Questions

## What's `stdint.h`?

stdint.h is a header file in the C standard library introduced in the C99 standard library section 7.18 to allow programmers to write more portable code by providing a set of typedefs that specify exact-width integer types, together with the defined minimum and maximum allowable values for each type

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

All of these are part of Windows Datatypes.

A uint8_t or BYTE corresponds to a single octet of bits, and determines depth of one of the three colors of RGB.

A uint32_t or DWORD used to describe metadata of picture, such as bitmap file size, type of compression, etc.

A int32_t or LONG used to describe wide range metadata, such as width or height of a bitmap.

A uint16_t or WORD used to describe short range metadata, such as  file type, the number of bits-per-pixel, etc.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE is an 8-bit unsigned value.
A DWORD is a 32-bit unsigned integer.
A LONG is a 32-bit signed integer. The first bit is signed bit.
A WORD is a 16-bit unsigned integer.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

BM
16973
0x424d

## What's the difference between `bfSize` and `biSize`?

bfSize
The size, in bytes, of the bitmap file.

biSize
The number of bytes required by the structure of BITMAPINFOHEADER.

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down DIB and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in `copy.c`?

The file doesn't exist.
The file is opened in a mode that doesn't allow other accesses.
The file exists, but we don't have permissions.

## Why is the third argument to `fread` always `1` in our code?

Because bitmaps always contains only one definition of BITMAPFILEHEADER and one definition of BITMAPINFOHEADER. And we are always reading triplets one by one in our main loop.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

 (4 - (3 * 3) % 4) % 4 = 3

## What does `fseek` do?

fseek sets the file position of the stream to the given offset.

## What is `SEEK_CUR`?

SEEK_CUR is the constant which tells fseek to make offset from the current position of file pointer.