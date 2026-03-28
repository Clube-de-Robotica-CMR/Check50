#include <stdio.h>

int calcular_moedas(int centavos);

int main()
{
    int troco; 
    do
    {
        printf("Troco devido: ");
        scanf("%i", &troco);
    } while (troco < 0);

    int moedas = calcular_moedas(troco);
    printf("%i\n", moedas);
}

int calcular_moedas(int centavos)
{
    int moedas = 0;
    while (centavos > 0)
    {
        if (centavos >= 25)
        {
            centavos -= 25;
            moedas++;
        } 
        else if (centavos >= 10)
        {
            centavos -= 10;
            moedas++;
        } 
        else if (centavos >= 5)
        {
            centavos -= 5;
            moedas++;
        }
        else
        {
            centavos--;
            moedas++;
        }
    }
    return moedas;
}