import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;

public class run{

    private static HashMap<String, Integer> dataPairs;
    private static ArrayList<ArrayList<Integer>> neighbours;
    //private static TreeMap<Integer, String> edges;

    public static void main(String[] args) throws IOException {

        long a = System.currentTimeMillis();
        readData();
        long b = System.currentTimeMillis();

        //System.out.println("TIME TO GATHER DATA: " + (b - a));

        solution2 s = new solution2(dataPairs, neighbours);

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

        //BufferedInputStream bis = new BufferedInputStream(new FileInputStream("data/secret/1small.in"));
        BufferedInputStream bis = new BufferedInputStream(new FileInputStream("data/secret/2med.in"));

        int people = readInt(bis) + 1;
        int pairs = readInt(bis);


        dataPairs = new HashMap<>();
        neighbours = new ArrayList<>(people);
	//edges = new TreeMap<>();

        for (int i = 0; i < people; i++) {
            neighbours.add(new ArrayList<>());
        }

        int c = 0;

        while (c < pairs) {

            int u = readInt(bis);
            int v = readInt(bis);
            int w = readInt(bis);

            String key = u + Integer.toString(v);

            dataPairs.put(key, w);
	    //edges.put(w, key);

            neighbours.get(u).add(v);
            neighbours.get(v).add(u);

            c++;
        }

        bis.close();
    }
}
