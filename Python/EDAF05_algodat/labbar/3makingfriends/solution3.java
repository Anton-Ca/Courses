
import java.util.*;

public class solution3 {

    private HashMap<String, Integer> dataPairs;
    private ArrayList<ArrayList<Integer>> vertices;

    /* ---------------------- Public Constructor ---------------------- */

    public solution3(HashMap<String, Integer> dataPairs, ArrayList<ArrayList<Integer>> vertices) {
        this.dataPairs = dataPairs;
        this.vertices = vertices;

        long a = System.currentTimeMillis();
        int [] graph = graph();
        long b = System.currentTimeMillis();

        //System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");

        long c = System.currentTimeMillis();
        System.out.println(prim(graph));
        long d = System.currentTimeMillis();

        //System.out.println("TIME TO EXECUTE ALGORITHM: " + (d - c) + "\n");

    }

    /* ---------------------- Private Methods ---------------------- */

    //Perform Prim's algorithm.
    private int prim(int [] graph) {
        PriorityQueue<Tuple> pool = new PriorityQueue<>(Comparator.comparingInt(tuple -> tuple.weight));

        pool.offer(new Tuple(graph[0], 0));

        HashSet<Integer> visited = new HashSet<>(vertices.size());

        int counter = 0;

        while (pool.size() > 0) {

            Tuple tuple = pool.poll();

            if (!visited.contains(tuple.vertex)) {

                counter += tuple.weight;
                visited.add(tuple.vertex);

                for (Integer vertex_v : vertices.get(tuple.vertex)) {

                    int weight = weight(tuple.vertex, vertex_v);

                    Tuple t = new Tuple(vertex_v, weight);

		    if (visited.contains(t.vertex))
			continue;

                    pool.offer(t);

                }
            }
        }
        return counter;
    }

    //Retrive weight between two vertices.
    private int weight(int vertex_u, int vertex_v) {

        String searchKeyOne = vertex_u + "-" + vertex_v;
        String searchKeyTwo = vertex_v + "-" + vertex_u;

        if (dataPairs.get(searchKeyOne) == null) {
            return dataPairs.get(searchKeyTwo);

        } else {
            return dataPairs.get(searchKeyOne);
        }
    }

    //Create graph consisting of ints.
    private int [] graph() {

        int [] vertexList = new int [vertices.size()];

        for (int i = 0; i < vertices.size(); i++ ) {

            vertexList[i] = i+1;

        }
        return  vertexList;
    }

    // Nested class to keep track of vertices and their edges.
    private static class Tuple {

        int vertex;
        int weight;

        public Tuple(int vertex, int weight) {
            this.vertex = vertex;
            this.weight = weight;
        }

        @Override
        public String toString() {
            return "Tuple{" +
                    "vertex=" + vertex +
                    ", weight=" + weight +
                    '}';
        }
    }

    /* ---------------------- End of code ---------------------- */

}

