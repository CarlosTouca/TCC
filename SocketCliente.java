import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

/**

 *

 * @author Mekhos

 */

public class SocketCliente {

   

public static void main(String[] args) throws IOException{

  Socket client = new Socket("192.168.15.201", 80);      /*criando uma conecxao para o servidor localizado

                                                         * em 192.169.1.201 porta 80

                                                         */

//Cria um canal para receber dados.



DataInputStream in=new DataInputStream(client.getInputStream());

//Cria um canal para enviar dados.

DataOutputStream out=new DataOutputStream(client.getOutputStream());

out.writeBytes("OI");       //enviando uma string

byte []array = new byte[20];
String s = in.readUTF(); //Aguarda o recebimento de uma string.

//in.read(array); //Aguarda o recebimento de uma string.

out.writeBytes("Obrigado!");      //enviando uma string

//System.out.println(array);      //imprimendo a string recebida

System.out.println(s);      //imprimendo a string recebida

//Fecha os canais de entrada e saída.

in.close();

out.close();

//Fecha o socket.

client.close();

 
    }

}
