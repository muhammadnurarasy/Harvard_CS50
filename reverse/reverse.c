#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *input = fopen(argv[1], "r");
    if (!input)
    {
        printf("Could not open file %s.\n", argv[1]);
        return 1;
    }

    // Read header
    // TODO #3
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    // TODO #4
    if (!check_format(header))
    {
        printf("Input is not a WAV file.\n");
        fclose(input);
        return 1;
    }

    // Open output file for writing
    // TODO #5
    FILE *output = fopen(argv[2], "w");
    if (!output)
    {
        printf("Could not open file %s.\n", argv[2]);
        fclose(input);
        return 1;
    }


    // Write header to file
    // TODO #6
    fwrite(&header, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    // TODO #7
    int block_size = get_block_size(header);

    // Write reversed audio to file
    // TODO #8
    uint8_t *block = malloc(block_size);
    if (!block)
    {
        printf("Memory allocation error.\n");
        fclose(input);
        fclose(output);
        return 1;
    }

    for (int i = header.subchunk2Size; i >= block_size; i -= block_size)
    {
        fseek(input, sizeof(WAVHEADER) + i - block_size, SEEK_SET);
        fread(block, block_size, 1, input);
        fwrite(block, block_size, 1, output);
    }

    free(block);
    fclose(input);
    fclose(output);

}

int check_format(WAVHEADER header)
{
    // TODO #4
    if (header.format[0] == 'W' && header.format[1] == 'A' &&
        header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 1;
    }
    return 0;
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    return header.numChannels * (header.bitsPerSample / 8);
}