import java.io.FileNotFoundException;
import java.util.Scanner;

public class run{

    private static int wordSize;
    private static int querySize;


    public static void main (String [] args) throws FileNotFoundException {

        String [] data = readData();
        solution s = new solution(wordSize, querySize, data);
    }

    //Reads data from input, sends to solution class.
    public static String [] readData() throws FileNotFoundException {
	// BuffertReader istället
        int counter = 0;
        Scanner scanner = new Scanner(System.in);

        wordSize = scanner.nextInt();
        querySize = scanner.nextInt();

        int allocateArray = wordSize + querySize*2;

        String [] data = new String [allocateArray];

        while(scanner.hasNext()) {
            data[counter] = scanner.next();
            counter++;
        }

        return data;
    }
}
