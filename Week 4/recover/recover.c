// Jorge Daniel Gómez Quintana "Recover"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: %s forensic_image\n", argv[0]);
        return 1;
    }

    // Open forensic image file
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    unsigned char buffer[512];
    int jpeg_count = 0;
    FILE *outptr = NULL;
    char filename[8];

    // Read the file in 512-bytes blocks
    while (fread(buffer, 1, 512, inptr) == 512)
    {
        // Check for JPEG signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous JPEG if open
            if (outptr != NULL)
            {
                fclose(outptr);
                jpeg_count++;
            }

            // Create new JPEG filename+
            sprintf(filename, "%03d.jpg", jpeg_count);
            outptr = fopen(filename, "w");
            if (outptr == NULL)
            {
                fclose(inptr);
                printf("Could not create %s.\n", filename);
                return 1;
            }
        }

        // Write block to current JPEG file is open
        if (outptr != NULL)
        {
            fwrite(buffer, 1, 512, outptr);
        }
    }

    // Close any remaining files
    if (outptr != NULL)
    {
        fclose(outptr);
    }
    fclose(inptr);

    return 0;
}
