import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.io.FileInputStream;

public class run4 {

    private static HashMap<String, Integer> dataPairs;
    private static ArrayList<ArrayList<Integer>> neighbours;

    public static void main(String[] args) throws IOException {
	
	long a = System.currentTimeMillis(); 
        readData();
	long b = System.currentTimeMillis();
        
	//System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");	
	
	solution3 s = new solution3(dataPairs, neighbours);

    }

    //Reads integers from input stream.
    private static int readInt(InputStream in) throws IOException {
        int ret = 0;
        boolean dig = false;

        for (int c; (c = in.read()) != -1; ) {
            if (c >= '0' && c <= '9') {
                dig = true;
                ret = ret * 10 + c - '0';
            } else if (dig) break;
        }

        return ret;
    }

    //Reads data from input, sends to solution class.
    private static void readData() throws IOException {

        //BufferedInputStream bis = new BufferedInputStream(new FileInputStream("data/secret/4huge.in"));
        BufferedInputStream bis = new BufferedInputStream(System.in);

        int people = readInt(bis) + 1;
        int pairs = readInt(bis);


        dataPairs = new HashMap<>();
        neighbours = new ArrayList<>(people);

        for (int i = 0; i < people; i++) {
            neighbours.add(new ArrayList<>());
        }

        int c = 0;

        while (c < pairs) {

            int u = readInt(bis);
            int v = readInt(bis);
            int w = readInt(bis);

            String key = u + "-" + v;

            dataPairs.put(key, w);

            neighbours.get(u).add(v);
            neighbours.get(v).add(u);

            c++;
        }

        bis.close();
    }
}
