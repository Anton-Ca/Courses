import java.util.*;
import java.util.Comparator;

public class solution2 {
	private HashMap<String, Integer> dataPairs;
	private ArrayList<ArrayList<Integer>> nodes;
	private static HashMap<String, Integer> dataPairsNode;

	public solution2(HashMap<String, Integer> dataPairs, ArrayList<ArrayList<Integer>> nodes) {
		this.dataPairs = dataPairs;
		this.nodes = nodes;
		dataPairsNode = dataPairs;

		long a = System.currentTimeMillis();
		ArrayList<Node> graph = createGraph();
		long b = System.currentTimeMillis();
	 	//System.out.println("TIME TO CREATE GRAPH: " + (b - a) + "\n");

		a = System.currentTimeMillis();
		System.out.println(prim(graph));
		b = System.currentTimeMillis();
	 	//System.out.println("TIME TO EXECUTE ALGORITHM: " + (b - a) + "\n");
	}

/* ------------------------------ Create Graph (add nodes) ------------------------------ */


	private ArrayList<Node> createGraph() {
		ArrayList<Integer> nodeList;
		ArrayList<Node> referenceList = new ArrayList<>(nodes.size());

		// Create all nodes (all references)
		for (int i = 1; i < nodes.size(); i++)
			referenceList.add(new Node(i));

		// Update neighbors
		for (int j = 0; j < referenceList.size(); j++) {
			Node n = referenceList.get(j);
			nodeList = nodes.get((n.index));

			for (int k = 0; k < nodeList.size(); k++)
				n.neighbours.put(nodeList.get(k), referenceList.get(nodeList.get(k) - 1));

		}
		return referenceList;
	}

/* ------------------------------ Performing Algorithm ------------------------------ */


	private int prim(ArrayList<Node> graph) {
		PriorityQueue<Tuple> pool = new PriorityQueue<>(Comparator.comparingInt(e -> e.weight));
		pool.offer(new Tuple(graph.get(0), 0));
		HashSet<Integer> visited = new HashSet<>();

		int counter = 0;

		while (pool.size() > 0) {
			Tuple edge = pool.poll();
			
			if (visited.contains(edge.startNode.index))
				continue;

			counter += edge.weight;
			visited.add(edge.startNode.index);

			for (Node endNode : edge.startNode.neighbours.values()) {
				Tuple T = new Tuple(endNode, edge.startNode.getWeight(endNode));
				pool.offer(T);

			}
		}
		return counter;
	}

/* ------------------------------ Nested classes ------------------------------ */


	private static class Node {
		int index;
		HashMap<Integer, Node> neighbours = new HashMap<>();
		HashMap<String, Integer> dataPairs = dataPairsNode;

		public Node(int index) {
			this.index = index;
		}

		int getWeight(Node n) {

			String searchKeyOne = this.index + "," + Integer.toString(n.index);
			String searchKeyTwo = n.index + "," + Integer.toString(this.index);

			if (dataPairs.get(searchKeyOne) == null) {
				return dataPairs.get(searchKeyTwo);
			} else {
				return dataPairs.get(searchKeyOne);
			}
		}

		@Override
		public String toString() {
			return " " + index;
		}
	}

	private static class Tuple {
		Node startNode;
		int weight;
		
		public Tuple(Node startNode, int weight) {
			this.startNode = startNode;
			this.weight = weight;
		}
	}
}
