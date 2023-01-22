import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.HashMap;

public class run3{

    private static HashMap<String, Integer> dataPairs;
    private static ArrayList<ArrayList<Integer>> neighbours;

    public static void main(String[] args) throws FileNotFoundException {
        long a = System.currentTimeMillis();
        readData();
        long b = System.currentTimeMillis();

        System.out.println("TIME TO GATHER DATA: " + (b - a));

        long c = System.currentTimeMillis();
        solution3 s = new solution3(dataPairs, neighbours);
        long d = System.currentTimeMillis();
        System.out.println("TIME TO GATHER DATA: " + (d - c));

    }


    //Reads data from input, sends to solution class.
    private static void readData() throws FileNotFoundException {
        File file = new File("data/secret/4huge.in");

	try {
	        Scanner scanner = new Scanner(file);
	
	        int people = scanner.nextInt();
	        int pairs = scanner.nextInt();
	
	
	        dataPairs = new HashMap<>();
	        neighbours = new ArrayList<>(people + 1);
	
	        for (int i = 0; i < people + 1; i++) 
	            neighbours.add(new ArrayList<>());
	        
	
	        int c = 0;
	
	        while (c < pairs){
	
	            int u = scanner.nextInt();
	            int v = scanner.nextInt();
	            int w = scanner.nextInt();
	
	            String key = u + "-" + Integer.toString(v);
	
	            dataPairs.put(key, w);
	
	            neighbours.get(u).add(v);
	            neighbours.get(v).add(u);
		    c++;
		}

	} catch (FileNotFoundException e) {
		e.printStackTrace();
	}
    }
}
