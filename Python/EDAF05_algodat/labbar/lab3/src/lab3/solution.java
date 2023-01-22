import java.util.*;
import java.util.TreeMap;
import java.util.Comparator;

public class solution2 {

	private HashMap<String, Integer> dataPairs;
	private ArrayList<ArrayList<Integer>> nodes;
	private static HashMap<String, Integer> dataPairsNode;
	private static ArrayList<Integer> nodeFrom;
	private static ArrayList<Integer> nodeTo;
	private static ArrayList<Integer> edges;

	public solution2(HashMap<String, Integer> dataPairs, ArrayList<ArrayList<Integer>> nodes){
		this.dataPairs = dataPairs;
		this.nodes = nodes;
		dataPairsNode = dataPairs;
		this.edges = edges;

		long a = System.currentTimeMillis();
		ArrayList<Node> graph = createGraph();
		long b = System.currentTimeMillis();

		// System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");

		// a = System.currentTimeMillis();
		// HashMap<Integer, Integer> MST = prim(graph);
		// System.out.println(prim(graph));
		// b = System.currentTimeMillis();

		// int answer = recTime(MST);
		// System.out.println(answer);
		a = System.currentTimeMillis();
		System.out.println(prim(graph));
		b = System.currentTimeMillis();
		// System.out.println("TIME TO EXECUTE ALGORITHM: " + (b - a) + "\n");

	}

	// @SuppressWarnings("unchecked")
	private ArrayList<Node> createGraph() {
		ArrayList<Integer> nodeList;
		ArrayList<Node> referenceList = new ArrayList<>(nodes.size());

		// Create all nodes (all references)
		for (int i = 1; i < nodes.size(); i++)
			referenceList.add(new Node(i));

		// Set distance and references in neighbour HashMap
		for (int j = 0; j < referenceList.size(); j++) {
			Node n = referenceList.get(j);

			if (j == 0)
				n.d = 0;

			for (int k = 0; k < (nodeList = nodes.get((n.index))).size(); k++)
				n.neighbours.put(nodeList.get(k), referenceList.get(nodeList.get(k) - 1));

		}
		return referenceList;
	}

	private int prim(ArrayList<Node> graph) {

		PriorityQueue<Tuple> pool = new PriorityQueue<>(Comparator.comparingInt(e -> e.weight));
		pool.offer(new Tuple(graph.get(0), 0));
		HashSet<Node> visited = new HashSet<>();

		int counter = 0;

		while (pool.size() > 0) {
			Tuple edge = pool.poll();

			// System.out.println("Current Node: " + edge.startNode.index);

			if (visited.contains(edge.startNode))
				continue;

			counter += edge.weight;
			visited.add(edge.startNode);

			for (Node endNode : edge.startNode.neighbours.values()) {
				// System.out.println("FROM " + edge.startNode.index + " TO " + endNode.index + " | NEIGHBOURS TO " + edge.startNode.index + ": " +u.startNode.neighbours.keySet());
				Tuple T = new Tuple(endNode, edge.startNode.getWeight(endNode));
				pool.offer(T);

			}
			// System.out.println("Counter: " + counter + " | Going From Node: " + edge.startNode.index + " To: " + pool.peek().startNode.index);

		}
		// System.out.println(visited.size() + " | " + graph.size());
		return counter;

	}

	private static class Node {

		int index;
		int d = Integer.MAX_VALUE;

		HashMap<Integer, Node> neighbours = new HashMap<>();
		HashMap<String, Integer> dataPairs = dataPairsNode;

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
		public String toString() {
			return " " + index + ".d = " + d + " ";
		}
	}

//	private static class Edge {
//
//		int index;
//		Node from;
//		Node to;
//
//		HashMap<String, Integer> dataPairs = dataPairsNode;
//
//		public Edge(Node n1, Node n2) {
//			this.from = n1;
//			this.to = n2;
//			index = n1.getWeight(n2);
//		}
//
//		@Override
//		public String toString() {
//			return "Edge = " + index + " | Node 1 = " + from.index + " | Node 2 = " + to.index;
//		}
//	}
//	
	private static class Tuple {
		Node startNode;
		int weight;

		public Tuple(Node startNode, int weight) {
			this.startNode = startNode;
			this.weight = weight;
		}

	}

}