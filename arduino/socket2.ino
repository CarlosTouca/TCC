/*

 *Autor: Mekhos

 *Descrisao: Codigo de um servidor web que esta com uma conexao de um cliente na porta 80

*/

#include <Ethernet.h>

#include <SPI.h>

byte mac[] = {

  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  //endereco mac

byte ip[] = {      

  192, 168, 15, 201 } ;    //endereço IP

EthernetServer server(80);  //criando um objeto do tipo servidor

int led = 7;
char dado;


void setup()

{

  Serial.begin(9600);

  Ethernet.begin(mac, ip);    //setando o ip e o mac para o arduino ser reconhecido na rede

  server.begin();        // levantando o servidor
  Serial.println("Pronto");
  pinMode(led,OUTPUT);
  
}

void loop()

{

  EthernetClient client = server.available();    /*servidor esperando uma requisicao, apos a

                                          requisicao ser encontrada a funcao retorna

                                          um objeto do tipo client

                                          */

  if (client) {    //testa se o exeiste

    while (client.connected()) {    //testa se o cliente esta conectado

     while (client.available()) {    //retorna o numero de byte no buffer de entrada

      dado = client.read();
      Serial.print((char)dado);

          if(dado == '1'){
            digitalWrite(led, HIGH);
          }
          else{
            digitalWrite(led, LOW);
          }
      

      }

    

      client.println("Bem vindo! a Toucatronic");    //envia para o cliente a seguinte String

      delay(2); // dá um tempo para  o cliente receber os caracteres

//       while (client.available()) {    //retorna o numero de byte no buffer de entrada
//
//      Serial.print(client.read());    
//
//      }
//
//      delay(2); // dá um tempo para  o cliente receber os caracteres

      client.stop();    //finaliza a conexao

      break;    //sai do loop

    }

   //while(1);    //loop infinito para evitar a finalizacao do programa

  }

}
