import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.*;

public class solution {

    private HashMap<Integer, ArrayList<Integer>> men;
    private HashMap<Integer, ArrayList<Integer>> women;
    private HashMap<Integer, Integer> pair;
    private String[] args;

    /* ---------------------- * TEST FILES * ---------------------- */

    String smallOne = "data/sample/1.in";

    String smallTwo = "data/sample/2.in";

    String zero = "data/secret/0testsmall.in";

    String one = "data/secret/1testsmallmessy.in";

    String two = "data/secret/2testmid.in";

    String three = "data/secret/3testlarge.in";

    String four = "data/secret/4testhuge.in";

    String five = "data/secret/5testhugemessy.in";

    /* ---------------------- * Main * ---------------------- */

    public static void main(String[] args) {
    	try {
			solution s = new solution(args);		
		} catch (IOException e) {
			System.out.println(e);
		}
    }
    
    /* ---------------------- * Constructor * ---------------------- */

    // Constructor that takes an input argument 
     public solution(String[] args) throws IOException {
    	  men = new HashMap<>();
    	  women = new HashMap<>();
    	  pair = new HashMap<>();

    	  System.out.println("GATHERING DATA...\n");

    	  for (String arg : args) {

    		  long a = System.currentTimeMillis();
    	  		readFile(arg);
    		  long b = System.currentTimeMillis();

    	  	System.out.println("\n!PERFORMING ALGORITHM!\n");

    	  	long c = System.currentTimeMillis();
    	  	// System.out.println("WOMAN 1: " + women.get(1).toString());
    	  	GaleShapely();
    	  	long d = System.currentTimeMillis();

    	  	printSolution();

    	  	System.out.println("\nTIME TO READ FILE (MS): " + Integer.parseInt(String.valueOf(b - a)));
    	  	System.out.println("TIME TO PERFORM ALORITHM (MS): " + Integer.parseInt(String.valueOf(d - c)));
    	  }

    	 
     }
    
    //Public constructor.
//    public solution() throws IOException {
//        men = new HashMap<>();
//        women = new HashMap<>();
//        pair = new HashMap<>();
//
//        System.out.println("GATHERING DATA...\n");
//
//        long a = System.currentTimeMillis();
//        readFile();
//        long b = System.currentTimeMillis();
//
//        System.out.println("\n!PERFORMING ALGORITHM!\n");
//
//        long c = System.currentTimeMillis();
//        // System.out.println("WOMAN 1: " + women.get(1).toString());
//        GaleShapely();
//        long d = System.currentTimeMillis();
//
//        printSolution();
//
//        System.out.println("\nTIME TO READ FILE (MS): " + Integer.parseInt(String.valueOf(b - a)));
//        System.out.println("TIME TO PERFORM ALORITHM (MS): " + Integer.parseInt(String.valueOf(d - c)));
//
//    }

    /* ---------------------- * PRIVATE METHODS * ---------------------- */

    //Prints solution to problem read by readFile.
    private void printSolution() {
        //pair.forEach((key, value) -> System.out.println("WOMAN: " + key + " MAN: " + value));
        pair.forEach((key, value) -> System.out.println(value));

    }
    
    //Reads from input file.
    private void readFile(String arg) throws IOException {

        Scanner scanner = new Scanner(new File(arg));
        int chunkSize = scanner.nextInt();

        while (scanner.hasNext()) {
            ArrayList<Integer> prefList = new ArrayList<>(chunkSize);

            //First integer is either a man or a woman.
            int key = scanner.nextInt();

            //Read the following integers in chunks.
            for (int i = 0; i < chunkSize; i++) {
                prefList.add(scanner.nextInt());
            }

            //First occurrence of key is a women, otherwise a man.
            if(women.containsKey(key)) {
                men.put(key, prefList);

            } else {
		ArrayList<Integer> inverted_prefList = new ArrayList<>(prefList); 
		
                //Inverts list for later comparison.
                for (int i = 0; i < chunkSize; i++) {
			inverted_prefList.set(prefList.get(i) - 1, i + 1); 
                }
			
                women.put(key, inverted_prefList);
            }
        }
        scanner.close();
    }
    //Reads from input file.
//    private void readFile() throws IOException {
//
//        Scanner scanner = new Scanner(new File(one));
//        int chunkSize = scanner.nextInt();
//
//        while (scanner.hasNext()) {
//            ArrayList<Integer> prefList = new ArrayList<>(chunkSize);
//
//            //First integer is either a man or a woman.
//            int key = scanner.nextInt();
//
//            //Read the following integers in chunks.
//            for (int i = 0; i < chunkSize; i++) {
//                prefList.add(scanner.nextInt());
//            }
//
//            //First occurrence of key is a women, otherwise a man.
//            if(women.containsKey(key)) {
//                men.put(key, prefList);
//
//            } else {
//		ArrayList<Integer> inverted_prefList = new ArrayList<>(prefList); 
//		
//                //Inverts list for later comparison.
//                for (int i = 0; i < chunkSize; i++) {
//			inverted_prefList.set(prefList.get(i) - 1, i + 1); 
//                }
//			
//                women.put(key, inverted_prefList);
//            }
//        }
//        scanner.close();
//    }

    //Uses Gale-Shapely-algorithm to decide good and stable pairs.
    private void GaleShapely() {

        PriorityQueue<Integer> pool = new PriorityQueue<>(men.keySet());

        while(pool.size() > 0) {
            int first = 0;
            int losing;

            //Retrieve first man: m and his most favorite (not yet proposed to) woman: w.
            int m = pool.poll();
            int w = men.get(m).get(first);

            //Makes it impossible for man: m to propose to woman: w again by removing her from his preference list
            men.get(m).remove(first);

            //Pairs man: m with woman: w if w is not yet paired
           if(!pair.containsKey(w)) {
               pair.put(w, m);

           //If woman: w has a husband but prefers man: m, break up the pair (w, losing) and replace it with the new one (w, m)
           } else if (m < (losing = pair.get(w))) {
	//	else if (women.get(w).get(m) < (losing = women.get(w).get(pair.get(w)))) { // Här blir det out of bounds 
        	         pool.offer(losing);
            		 pair.replace(w, losing, m);

           } else {
               pool.offer(m);
           }
        }
    }

    /* ---------------------- * END OF CODE * ---------------------- */
}
