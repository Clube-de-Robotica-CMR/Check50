#include <stdio.h>
#include <stdlib.h>

int main()
{
    int h;
    do
    {
        printf("Altura: ");
        scanf("%i", &h);
    } while (h < 1 || h > 8);

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