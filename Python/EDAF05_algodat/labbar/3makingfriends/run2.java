import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;

public class run2{

    private static HashMap<String, Integer> dataPairs;
    private static ArrayList<ArrayList<Integer>> neighbours;

    public static void main(String[] args) throws IOException {

        long a = System.currentTimeMillis();
        readData();
        long b = System.currentTimeMillis();

        //System.out.println("TIME TO GATHER DATA: " + (b - a));

        solution3 s = new solution3(dataPairs, neighbours);

    }

    //Reads integers from input stream.
    private static int readInt(BufferedReader in) throws IOException {
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

	BufferedReader br = new BufferedReader (new InputStreamReader(System.in));	

        int people = readInt(br) + 1;
        int pairs = readInt(br);


        dataPairs = new HashMap<>();
        neighbours = new ArrayList<>(people);

        for (int i = 0; i < people; i++) {
            neighbours.add(new ArrayList<>());
        }

        int c = 0;

        while (c < pairs) {

            int u = readInt(br);
            int v = readInt(br);
            int w = readInt(br);

            String key = u + "-" + Integer.toString(v);

            dataPairs.put(key, w);

            neighbours.get(u).add(v);
            neighbours.get(v).add(u);

            c++;
        }

        br.close();
    }
}
