package lab2;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class Path {
    private ArrayList<String> words;
    private String[][]  queries;

	public static void main(String[] args) {
		try {
		Path pt = new Path();
		} catch (IOException e) {
			System.out.println("We got an unhandled issue over here");
		}
	}

	/* ---------------------- * TEST FILES * ---------------------- */

	String test = "data/sample/1.in";

	String smallOne = "data/sample/1small1.in";

	String smallTwo = "data/secret/2small2.in";

	String three = "data/secret/3medium1.in";

	String four = "data/secret/4medium2.in";

	String five = "data/secret/5large1.in";

	String six = "data/secret/6large2.in";

	/* ---------------------- * Constructor * ---------------------- */
	
	public Path() throws IOException{
		System.out.println("GATHERING DATA...\n");


  		long a = System.currentTimeMillis();
  	  		readFile();
  		long b = System.currentTimeMillis();

  	  	System.out.println("\n!PERFORMING ALGORITHM!\n");

  	  	long c = System.currentTimeMillis();
  	  	long d = System.currentTimeMillis();

  	  	System.out.println("\nTIME TO READ FILE (MS): " + Integer.parseInt(String.valueOf(b - a)));
  	  	System.out.println("TIME TO PERFORM ALORITHM (MS): " + Integer.parseInt(String.valueOf(d - c)));
	}
	
	/* ---------------------- * Constructor * ---------------------- */
	
	// Reads from input file.
	private void readFile() throws IOException {

        Scanner scanner = new Scanner(new File(smallTwo));
        String w = scanner.next();
        String q = scanner.next();
        

       words = new ArrayList<>(Integer.parseInt(w));
       queries = new String[Integer.parseInt(q)][1]; // Vilken datastructur passar för q?
       
       
       for (int i = 0; i < Integer.parseInt(w); i++)
    	   words.add(w);
       
       for (int i = 0; i < Integer.parseInt(q); i++) {
    	   String[] splitString = scanner.nextLine().split(" ", 1);
    	   for (int j = 0; j < 2; j++)
    		   queries[i][j] = splitString[j];
    	   
       }
        scanner.close();
    }

}
