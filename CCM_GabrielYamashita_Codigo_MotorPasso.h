#ifndef MOTORPASSO_H // Caso MOTORPASSO_H não exista entra no if
#define MOTORPASSO_H // Cria o MOTORPASSO_H
#include "mbed.h" // Importa Biblioteca do mbed

class MP { // Inicialização da Classe MP (Motor de Passo)
    public:
        MP(PinName A, PinName B, PinName C, PinName D, PinName E, PinName F); // EnA, A+, A-, EnB, B+, B-
        
        // Métodos:
        void MoverMotor(bool EN, int DIR); // Método para Mover 1 passo do Motor
        void FasesBobinas(int fase); // Método para Ativar as Bobinas com a Fase do Array
        float setVelocidade(int velRPM); // Define a Velocidade do Motor em ms
        float Map(float value, float fromLow, float fromHigh, float toLow, float toHigh); // Converte a Velocidade de RPM para ms

        // GPIO's (acionamentos do motor de passo):
        DigitalOut ENA;
        DigitalOut AP;
        DigitalOut AM;
        DigitalOut ENB;
        DigitalOut BP;
        DigitalOut BM;
        
        // Variáveis:
        int fases[4]; // Declaração do Array das Fases dos Motores
        int velocidadeRPM; // Declaração da Velocidade RPM
        int Passo; // Declaração do Passo para Controle do Array
};

#endif // Final do if
