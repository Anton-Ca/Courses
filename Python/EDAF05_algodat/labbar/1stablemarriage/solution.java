import java.util.*;

public class solution {

    private int [] data;

    private HashMap<Integer, ArrayList<Integer>> men;
    private HashMap<Integer, ArrayList<Integer>> women;

    private int [] pair;
    private int chunkSize;


    //Public constructor.
    public solution(int [] data, int size) {
        this.data = data;

        chunkSize = size;

        men = new HashMap<>(chunkSize);
        women = new HashMap<>(chunkSize);
        pair = new int [chunkSize + 1];

        long a = System.currentTimeMillis();
        readInput();
        long b = System.currentTimeMillis();
        GaleShapely();
        long c= System.currentTimeMillis();
        printSolution();

        //System.out.println("TIME TO SET UP: " + (b - a) + " MS");
        //System.out.println("TIME TO EXECUTE ALGORITHM: " + (c - b) + " MS");

    }


    /* ---------------------- * PRIVATE METHODS * ---------------------- */

    //Prints i rows, where output is man: m paired with woman: i
    private void printSolution() {

       for (int i = 1; i <= chunkSize; i++) {
           System.out.println(pair[i]);
       }

    }

    //Reads from input file.
    private void readInput() {

       for (int i = 0; i < chunkSize*2; i++) {

            ArrayList<Integer> prefList = new ArrayList<>(chunkSize);

            int keyIndex = i*(chunkSize + 1);

            //Either man or woman.
           int key = data[keyIndex];

           //Read the following integers in chunks.
            for (int j = keyIndex + 1; j < keyIndex + chunkSize + 1; j++) {
                prefList.add(data[j]);
            }

            //First occurrence of key is a women, otherwise a man.
            if(women.containsKey(key)) {
                men.put(key, prefList);

            } else {

                ArrayList<Integer> invertedPrefList = new ArrayList<>(prefList);
                for (int k = 0; k < chunkSize; k++) {

                    int element = prefList.get(k) - 1;
                    invertedPrefList.set(element, k + 1);
                }

                women.put(key, invertedPrefList);

            }
        }
    }

    //Uses Galen-Shapely-algorithm to decide good and stable pairs.
    private void GaleShapely() {

//        PriorityQueue<Integer> pool = new PriorityQueue<>(men.keySet());
	ArrayList<Integer> pool = new ArrayList<>(men.keySet());
        while(pool.size() > 0) {
	        int first = 0;
		int last = pool.size()-1;

            //Retrieve first man: m and his most favorite (not yet proposed to) woman: w.
//              int m = pool.poll();
//              int w = men.get(m).get(first);
		int m = pool.get(last);
		pool.remove(last);
		int w = men.get(m).get(last);

            //Makes it impossible for man: m to propose to woman: w again by removing her from his preference list
            	men.get(m).remove(last);

            //Pairs man: m with woman: w if w is not yet paired
            if(pair[w] == 0) {
                pair[w] = m;

                //If woman: w has a husband but prefers man: m, break up the pair (w, losing) and replace it with the new one (w, m)
            } else if (women.get(w).get(m - 1) < women.get(w).get(pair[w] - 1)) {
//                pool.offer(pair[w]);
//                pair[w] = m;
	  	  pool.add(pair[w]);
		  pair[w] = m;

            } else {
                  pool.add(m);
            }
        }
    }

    /* ---------------------- * END OF CODE * ---------------------- */
}
