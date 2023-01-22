import java.util.*;
import java.util.TreeMap;
import java.util.Comparator;

public class solution {

    private HashMap<String, Integer> dataPairs;
    private ArrayList<ArrayList<Integer>> nodes;
    private static HashMap<String, Integer> dataPairsNode;
    //private static TreeMap<Integer, String> edges;

    public solution(HashMap<String, Integer> dataPairs, ArrayList<ArrayList<Integer>> nodes/*, TreeMap<Integer, String> edges*/) {
        this.dataPairs = dataPairs;
        this.nodes = nodes;
        dataPairsNode = dataPairs;
	//this.edges = edges;
        
        long a = System.currentTimeMillis();
        PriorityQueue<Node> graph = createGraph();
        long b = System.currentTimeMillis();

        //System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");

        //a = System.currentTimeMillis();
	//HashMap<Integer, Integer> MST = prim(graph);
	//System.out.println(prim(graph));
        //b = System.currentTimeMillis();
	
//	int answer = recTime(MST);	
//	System.out.println(answer);
        a = System.currentTimeMillis();
	System.out.println(prim(graph));
        b = System.currentTimeMillis();
        //System.out.println("TIME TO EXECUTE ALGORITHM: " + (b - a) + "\n");

    }
    @SuppressWarnings("unchecked")
    private PriorityQueue<Node> createGraph() {
	// Vi behöver ha någon sorts datastruktur som håller koll på kanterna och som vi sedan kan jämföra två objekt med Comparator nedan. Vi vill alltså jämföra kanterna sinsemellan och plocka ut den med minst avstånd (kant a - kant b) och det är inte noderna som vi ska sortera.
        ArrayList<Integer> nodeList;
        ArrayList<Node> referenceList = new ArrayList<>(nodes.size());
        PriorityQueue<Node> graph = new PriorityQueue<>(nodes.size(), edges); 
        //PriorityQueue<Node> graph = new PriorityQueue<>(nodes.size(), ((n1, n2) -> ((Comparable<Integer> )Integer.valueOf(dataPairs.get(n1))).compareTo(Integer.valueOf(dataPairs.get(n2))))); 
        //PriorityQueue<Node> graph = new PriorityQueue<>(nodes.size(), Comparator.comparingInt(n -> n.d)); 

        //Create all nodes (all references)
        for (int i = 1; i < nodes.size(); i++) 
            referenceList.add(new Node(i));

        //Set distance and references in neighbour HashMap
        for (int j = 0; j < referenceList.size(); j++) {
            Node n = referenceList.get(j);

            if (j == 0) 
                n.d = 0;

            for (int k = 0; k < (nodeList = nodes.get((n.index))).size(); k++) 
                n.neighbours.put(nodeList.get(k), referenceList.get(nodeList.get(k) - 1));
            
            graph.add(n);
        }
        return graph;
    }


    private int prim(PriorityQueue<Node> pool) {

	HashSet<Integer> visited = new HashSet<>();
	int counter = 0;
        //System.out.println(Arrays.toString(pool.toArray()));

        while (pool.size() > 0) {
            Node u = pool.poll();

	    if (visited.contains(u.index))
	    	continue;
	    	
	    counter += u.d;
	    visited.add(u.index);
	    // Uppdaterar avstånd från den utplockade noden u till alla grannar v uppdateras. 
            for (Node v : u.neighbours.values()) {
			//System.out.println("CURRENT NODE: " + u.index + " | NEIGHBOURS: " +  u.neighbours.keySet());
            		System.out.println("FROM " + u.index + " TO " + v.index + " | NEIGHBOURS TO " + u.index + ": " +  u.neighbours.keySet());
			pool.remove(v);
			//System.out.println("NEIGHBOURS TO NODE " + u.index + ": "+  u.neighbours.keySet());
                    	//v.d = u.d + u.getWeight(v);
                    	//v.p = u;
			Node duplicateNode = new Node(v.index);
			duplicateNode.d = u.getWeight(v);
			duplicateNode.neighbours = v.neighbours;
			duplicateNode.dataPairs = v.dataPairs;
			pool.offer(duplicateNode);
            		//System.out.println("NEIGHBOURS d VALUES: " + Arrays.toString(pool.toArray()) + "\n");
				
            }
        }
        return counter;
        
    }

    private static class Node {

        int index;
        int d = Integer.MAX_VALUE;
	boolean visited = false; 
        Node p;
	ArrayList<Integer> edges;

        HashMap<Integer, Node> neighbours = new HashMap<>();
        HashMap<String, Integer> dataPairs = dataPairsNode;

	for ()



        public Node(int index) {
            this.index = index;
        }

        int getWeight(Node n) {

            String searchKeyOne = this.index + Integer.toString(n.index);
            String searchKeyTwo = n.index + Integer.toString(this.index);

            if (dataPairs.get(searchKeyOne) == null) {
                return dataPairs.get(searchKeyTwo);
            } else {
                return dataPairs.get(searchKeyOne);
            }
        }
	@Override
    	private int compareTo(Node n1, Node n2){
    		if (n1 == null || n2 == null)
			return null;
    		return Integer.compare(n1.dataPairs);
    	
    	}
	@Override
    	public boolean equals(Object obj) {
    		if (obj instanceof Node) {
			return this.getWeight((Node) obj) == ((Node) obj).getWeight();
		} else {
			return false;
		}
	}


        @Override
        public String toString() {
            return " " + index + ".d = " + d + " ";
        }
    }
}
