#include "MotorPasso.h" // Importa Arquivo de Classe do Motor de Passo

MP::MP(PinName A, PinName B, PinName C, PinName D, PinName E, PinName F): // Inicialização da Classe MP
    ENA(A), AP(B), AM(C), ENB(D), BP(E), BM(F) { // Entradas de Ativação do Motor
    
    this -> fases[0] = 110110; // Fase de Ativação da Bobina || 0
    this -> fases[1] = 101110; // Fase de Ativação da Bobina || 1
    this -> fases[2] = 101101; // Fase de Ativação da Bobina || 2
    this -> fases[3] = 110101; // Fase de Ativação da Bobina || 3
}

void MP::MoverMotor(bool EN, int DIR) { // Método para Mover 1 passo do Motor
    if(EN == true) { // Checa se o Motor pode Ativar
        if(DIR == 0) { // Direção Sentido Horário
            this -> Passo++; // Aumenta o Contador da Bobina
            if(Passo >= 4) {this -> Passo=0;} // Volta para o Começo do Array de Bobinas
        }
        
        else if(DIR == 1) { // Direção Sentido Anti-Horário
            this -> Passo--; // Diminui o Contador da Bobina
            if(Passo <= -1) {this -> Passo=3;} // Volta para o Começo do Array de Bobinas
        }
        FasesBobinas(fases[Passo]); // Define a Fase da Bobina para cada Entrada
    }
}

void MP::FasesBobinas(int fase) { // Método para Ativar as Bobinas com a Fase do Array
    ENA = (fase/100000) % 10;
    AP =  (fase/ 10000) % 10;
    AM =  (fase/  1000) % 10;
    ENB = (fase/   100) % 10;
    BP =  (fase/    10) % 10;
    BM =  (fase/     1) % 10;
}

float MP::setVelocidade(int velRPM) { // Define a Velocidade do Motor em ms
    this -> velocidadeRPM = Map(velRPM, 10, 150, 30, 2);
    return this -> velocidadeRPM;
}

float MP::Map(float value, float fromLow, float fromHigh, float toLow, float toHigh) { // Converte a Velocidade de RPM para ms
    float toValue = (toHigh - toLow)/(fromHigh - fromLow) * (value - fromLow) + toLow;
    return toValue;
}
