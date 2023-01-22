import java.util.*;

public class solution {

    private final static int MAX_CHAR = 256;

    private String [] data;
    private Node [] graph;

    private int [] arcSize;
    private int[][] arcMatrix;

    private int wordSize;
    private int querySize;

    public solution(int wordSize, int querySize, String [] data) {

        this.wordSize = wordSize;
        this.querySize = querySize;
        this.data = data;

        //Initialize various data structures.
        arcMatrix = new int[wordSize][wordSize];
        arcSize = new int[wordSize];

        //Set up class.
        setupClass();
	
//	long t1 = System.currentTimeMillis();
        //Solve problems.
        solve();
//	long t2 = System.currentTimeMillis();
//	System.out.println("TIME TO PERFORM ALGORITHM: " + (t2 - t1) + " MS");
	
    }

    /* ---------------------- PRIVATE METHODS ----------------------*/

    //Sets up class by calling all required methods.
    private void setupClass() {
        fillMatrix();
        createArcs();
        graph = createGraph();
    }

    //Fills matrix with 0's.
    private void fillMatrix() {
        for (int i = 0; i < wordSize; i++) {
            for (int j = 0; j < wordSize; j++) {
                arcMatrix[i][j] = 0;
            }
        }
    }

    //Solves problem and prints to console.
    public void solve() {

        for (int i = 0; i < querySize; i++) {

            int startIndex = findIndex(data[(wordSize + (i * 2))]);
            int endIndex = findIndex(data[(wordSize + (i * 2) + 1)]);

            if (startIndex == endIndex) {
                System.out.println(0);

            } else {
                Breadth_First_Search(graph, startIndex, endIndex);
                resetNodes();
            }

        }
    }

    //Count characters in word.
    private HashMap<Character, Integer> mapDuplicates(String word) {

        HashMap<Character, Integer> map = new HashMap<>(wordSize);

        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);

            if (map.containsKey(c)) {
                int cnt = map.get(c);
                map.put(c, ++cnt);

            } else {
                map.put(c, 1);
            }
        }

        map.entrySet().removeIf(e -> e.getValue() < 2);
        return map;
    }

    //True if word2 contain >= duplicates of a specific character to word1, else false.
    private boolean isAllowedDuplicates(String word1, String word2) {

        Map<Character, Integer> w1 = mapDuplicates(word1);
        Map<Character, Integer> w2 = mapDuplicates(word2);

        for (char ch : w1.keySet()) {
            if (w2.get(ch) == null || w2.get(ch) < w1.get(ch)) {
                return false;
            }
        }

        return true;
    }


    //Returns false if string contains duplicates else true.
    public boolean isUnique(String word) {

        boolean[] chars = new boolean[MAX_CHAR];
        Arrays.fill(chars, false);

        for (int i = 0; i < word.length(); i++) {
            int index = word.charAt(i);

            //If the value is already true, string has duplicate characters, return false.
            if (chars[index]) {
                return false;
            }

            chars[index] = true;
        }
        //No duplicates encountered, return true.
        return true;
    }


    //True if all chars in substring u are present in string v.
    public boolean isPresent(String subString_u, String v) {

        for (int i = 0; i < subString_u.length(); i++) {

            if (v.indexOf(subString_u.charAt(i)) == -1) {
                return false;
            }
        }
        return true;
    }

    //Put a 1 into matrix [i, j] if there is an arc otherwise 0.
    private void createArcs() {
        int sub_startIndex = 1;

        for (int i = 0; i < wordSize; i++) {
            String u = data[i];

            for (int j = 0; j < wordSize; j++) {
                if (i != j) {

                    String v = data[j];
                    String subString_u = u.substring(sub_startIndex);

                    if (isPresent(subString_u, v)) {

                        if (isUnique(subString_u) || (!isUnique(subString_u) && isAllowedDuplicates(subString_u, v))) {
                            arcMatrix[i][j] = 1;
                            arcSize[i]++;
                        }
                    }
                }
            }
        }
    }

    //Create node-graph (list of nodes) from arc matrix.
    private Node[] createGraph() {

        Node[] graph = new Node[wordSize];

        //Fill graph with nodes.
        for (int i = 0; i < wordSize; i++) {

            //If has arcs, create new node with neighbours, else node without neighbours
            if (arcSize[i] != 0) {

               ArrayList<Integer> neighbours = new ArrayList<>(arcSize[i]);

                for (int j = 0; j < wordSize; j++) {
                    if (arcMatrix[i][j] == 1) {
                        neighbours.add(j);
                    }
                }
                graph[i] = new Node(i, neighbours);

            } else {
                graph[i] = new Node(i, new ArrayList<>());
            }
        }

        return graph;
    }

    private int findIndex (String string) {

        for (int i = 0; i < wordSize; i++) {

            if (data[i].equals(string)) {
                return i;
            }
        }
        return -1;
    }

    private void resetNodes() {

        for(Node n : graph) {
            if(!n.notVisited) {
                n.notVisited = true;
            }
        }
    }

    private void Breadth_First_Search(Node [] graph, int startNode, int endNode) {

        int w;
        graph[startNode].setVisited(startNode);

        LinkedList<Integer> nodePool = new LinkedList<>();
        nodePool.addFirst(startNode);

        while (nodePool.size() > 0) {

            int v = nodePool.removeFirst();

            for (int i = 0; i < graph[v].neighbours.size(); i++) {

                if((graph[(w = graph[v].neighbours.get(i))].notVisited)) {

                    graph[w].setVisited(v);
                    nodePool.addLast(w);

                    if(w == endNode) {
                        System.out.println(countPath(graph[w], startNode));
                        return;
                    }
                }
            }
        }
        System.out.println("Impossible");
    }

    //Recursively counts path from node: n to first node index.
    private int countPath(Node n, int startIndex) {

        if (n.wordsIndex == startIndex) {
            return 0;

        } else {
            return 1 + countPath(graph[n.pred], startIndex);
        }
    }

    //Nested class, use to create a node from a given word.
    private static class Node {

        int wordsIndex;
        int pred;
        ArrayList<Integer> neighbours;
        boolean notVisited = true;

        public Node(int wordsIndex, ArrayList<Integer> neighbours) {
            this.wordsIndex = wordsIndex;
            this.neighbours = neighbours;
        }

        //Node has been visited, set pred. to whichever node just visited this one.
        private void setVisited(int pred) {
            this.pred = pred;
            notVisited = false;
        }
    }


}
