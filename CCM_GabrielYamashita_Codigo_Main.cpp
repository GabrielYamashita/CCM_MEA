 
#include "mbed.h" // Importa Biblioteca do mbed
#include "MotorPasso.h" // Importa a Classe do Motor de Passo || MP

Serial pc(USBTX, USBRX, 9600); // Comunicação Serial

MP MPA(D2, D5, D4, A4, A0, A1); // Objeto de Motor || Motor B
MP MPB(D6, D9, D10, D11, D12, D13); // Objeto de Motor || Motor A

Ticker flipper1; // Timer para o Motor A
Ticker flipper2; // Timer para o Motor B

char comando; // Comando Recebido pela Serial

bool EMERG = false; // Flag de Emergência
bool ENA = false; // Enable do Motor A
bool ENB = false; // Enable do Motor B
int DIRA = 0; // Direção Horária Padrão do Motor A
int DIRB = 0; // Direção Horário Padrão do Motor B
int RPMA = 150; // Velocidade Padrão do Motor A
int RPMB = 150; // Velocidade Padrão do Motor B

bool FLIPA = false; // Flag do Timer do Motor A
bool FLIPB = false; // Flag do Timer do Motor B

int minRPM = 10;  // Velocidade Mínima do Motor
int stepRPM = 10; // Quanto a Velocidade Muda
int maxRPM = 150; // Velocidade Máxima do Motor


void callback() { // Função para Setar as Variáveis de Controle dos Motores
    comando = pc.getc(); // Recebe o Carácter da Serial
    
    // MOTOR A
    if(comando == '<') { // Diminui Velocidade do Motor A
        FLIPA = true; // Flag para Dizer que Diminui Velocidade
        RPMA -= stepRPM;
        if(RPMA < minRPM) {RPMA = minRPM;} // Checa se a Velocidade está Menor do que a Mínima
        pc.printf("Velocidade do Motor A -%d (%d). [<]\r\n", stepRPM, RPMA);
    }
    else if(comando == '>') { // Aumenta Velocidade do Motor A
        FLIPA = true; // Flag para Dizer que Aumenta Velocidade
        RPMA += stepRPM;
        if(RPMA > maxRPM) {RPMA = maxRPM;} // Checa se a Velocidade está Maior do que a Máxima
        pc.printf("Velocidade do Motor A +%d0 (%d). [>]\r\n", stepRPM, RPMA);
    }
    
    // MOTOR B
    else if(comando == '-') { // Diminui Velocidade do Motor B
        FLIPB = true; // Flag para Dizer que Diminui Velocidade
        RPMB -= stepRPM;
        if(RPMB < minRPM) {RPMB = minRPM;} // Checa se a Velocidade está Menor do que a Mínima
        pc.printf("Velocidade do Motor B -%d (%d). [-]\r\n", stepRPM, RPMB);
    }
    else if(comando == '+') { // Aumenta Velocidade do Motor B
        FLIPB = true; // Flag para Dizer que Aumenta Velocidade
        RPMB += stepRPM;
        if(RPMB > maxRPM) {RPMB = maxRPM;} // Checa se a Velocidade está Maior do que a Máxima
        pc.printf("Velocidade do Motor B +%d (%d). [+]\r\n", stepRPM, RPMB);
    }
    
    else if(EMERG == false) { // Checa se a Emergência está Acionada  
        // MOTOR A:
        if(comando == 'e') { // Ativa o Motor A
            ENA = true;            
            pc.printf("Motor A ativado. [e]\r\n");
        }
        else if(comando == 'd') { // Desativa o Motor A || false
            ENA = false;            
            pc.printf("Motor A desativado. [d]\r\n");
        }
        else if(comando == 'h') { // Muda o Sentido do Motor A, para Horário || 0
            DIRA = 0; // Sentido Horário
            pc.printf("Sentido do Motor A no sentido Horario. [h]\r\n");
        }
        else if(comando == 'a') { // Muda o Sentido do Motor A, para Anti-Horário || 1
            DIRA = 1; // Sentido Anti-horário
            pc.printf("Sentido do Motor A no sentido Anti-Horario. [a]\r\n");  
        }
        
        // MOTOR B:
        else if(comando == 'E') { // Ativa o Motor B || true
            ENB = true;
            pc.printf("Motor B ativado. [E]\r\n");
        }
        else if(comando == 'D') { // Desativa o Motor B || false
            ENB = false;
            pc.printf("Motor B desativado. [D]\r\n");
        }
        else if(comando == 'H') { // Muda o Sentido do Motor B, para Horário || 0
            DIRB = 0;
            pc.printf("Sentido do Motor B no sentido Horario. [H]\r\n");
        }
        else if(comando == 'A') { // Muda o Sentido do Motor B, para Anti-Horário || 1
            DIRB = 1;
            pc.printf("Sentido do Motor B no sentido Anti-Horario. [A]\r\n");
        }
        
        else if(comando == '!') { // Emergência
            ENA = 0; // Disable do Motor A
            ENB = 0; // Disable do Motor B
            EMERG = true;
            pc.printf("Entrando no Estado de Emergencia. [!]\r\n");
        }
        else if(comando == 'q') { // Comando para Sair da Aplicação
            pc.printf("Saindo da Aplicacao. [q]\r\n");
            wait_ms(1);
            NVIC_SystemReset(); // Reset da Núcleo
        }
    }
    
    else if(EMERG == true && comando == '!') { // Simulação da Retenção do Botão de Emergência
        EMERG = false;
        pc.printf("Saindo do Estado dde Emergencia. [!]\r\n");
    } 
    else { // Mostra que o Botão de Emergência não Está Solto Ainda
        pc.printf("Aperte o Botao de Emergencia para Sair do Estado de Emergencia.\r\n");
    }
}

void mA() { // Acionamento do Motor A
    MPA.MoverMotor(ENA, DIRA);
}

void mB() { // Acionamento do Motor B
    MPB.MoverMotor(ENB, DIRB);
}

int main() { // Função Main
    pc.attach(&callback); // Espera Entrada de Informação da Serial
    flipper1.attach(&mA, MPA.setVelocidade(RPMA)/1000); // Timer de Acionamento do Motor A || Velocidade do Motor A
    flipper2.attach(&mB, MPB.setVelocidade(RPMB)/1000); // Timer de Acionamento do Motor B || Velocidade do Motor B
    
    while(1) { // Loop Principal
        if(FLIPA == true) { // Checa se Ouve Mudança de Velocidade com a Flag do Motor A
            flipper1.attach(&m1, MPA.setVelocidade(RPMA)/1000); // Redefine Timer de Velocidade do Motor B
            FLIPA = false;
        }
        
        if(FLIPB == true) { // Checa se Ouve Mudança de Velocidade com a Flag do Motor B
            flipper2.attach(&m2, MPB.setVelocidade(RPMB)/1000); // Redefine Timer de Velocidade do Motor B
            FLIPB = false;
        }
    }
}
