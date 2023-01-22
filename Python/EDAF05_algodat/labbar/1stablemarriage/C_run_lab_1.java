import java.util.Scanner;

public class C_run_lab_1 {

    private static int size;


    public static void main (String [] args) {

        solution s = new solution(readData(), size);
    }

    //Reads data from input, sends to solution class.
    public static int [] readData() {

        int counter = 0;
        Scanner scanner = new Scanner(System.in);

        size = scanner.nextInt();

        int [] data = new int [2*size*size + 2*size];

        while(scanner.hasNext()) {
            data[counter] = scanner.nextInt();
            counter++;
        }

        return  data;
    }
}
