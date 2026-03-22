#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    int h = atoi(argv[1]);

    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h; j++)
        {
            if (j >= h - i - 1)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }

        printf("  ");

        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}