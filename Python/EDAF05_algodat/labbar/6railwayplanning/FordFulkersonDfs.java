import static java.lang.Math.min;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


// Del 2) Ta bort edges: Det vi vill göra är att använda oss av "Ta bort edges listan" för att få reda på vilka edges som ska bort. Vi bygger upp vår graf och tar bort alla edges i listan med "Ta bort edges". Sedan lägger vi till edges bakifrån från listan och håller koll på när vi uppnår capcaciteten som motsvarar kolumn 3 av indatan. Vi tar alltså listan går igenom bakifrån och uppdaterar vår halvfärdiga graf genom att lägga till några av de edges vi just tog bort  

public class FordFulkersonDfs extends NetworkFlowSolver {
	
	public static void main(String[] args) throws FileNotFoundException {
		
		long a = System.currentTimeMillis();
		DataTuple data = readData();
		long b = System.currentTimeMillis();
		//System.out.println("TIME TO GATHER DATA: " + (b - a));

		int n = data.nbrNodes;
		int s = data.nbrNodes-2;
		int t = data.nbrNodes-1;

		long c = System.currentTimeMillis();
		FordFulkersonDfs solver;
	    	solver = new FordFulkersonDfs(n, s, t);

		System.out.println("NUMBER OF NODES: " + n + " NUMBER OF EDGES: " + data.nbrEdges);
		System.out.println("INDEX OF SOURCE: " + n + " INDEX OF SINK: " + data.nbrEdges);
	    
	    	for (int i = 0; i < data.nbrEdges; i++) {
			int from = data.edges.get(i).from;
			int to = data.edges.get(i).to;
			long cap = data.edges.get(i).capacity;

	    		solver.addEdge(from, to, cap);
	    	}
		long d = System.currentTimeMillis();

		//System.out.println(solver);

		//System.out.println("TIME TO BUILD GRAPH: " + (d - c));
			
		long e = System.currentTimeMillis();
		System.out.println(solver.getMaxFlow());
		//solver.getMaxFlow();
		long f = System.currentTimeMillis();
		//System.out.println("TIME TO PERFORM ALGORITHM: " + (f - e));

		for (int i = 0; i < data.nbrRoutes; i++) {
			System.out.println(data.removeEdges[i]);
		}

		for (int i = 0; i < n; i++) {
			for (int j = 0; j < solver.getGraph()[i].size(); j++) {

				// Count residual edges
				if (solver.getGraph()[i].get(j).capacity != 0){

				long cap1 = solver.getGraph()[i].get(j).capacity;
				long fr1 = solver.getGraph()[i].get(j).from;
				long to1 = solver.getGraph()[i].get(j).to;
				
				System.out.println(to1 + " " + fr1 + " " + cap1);
				//System.out.println("EDGE  " + to1 + " " + fr1 + " " + cap1 + "   RESIDUAL  " + to2 + " " + fr2 + " " + cap2);
				}
			}
		} 
	}

/* ------------------------------ Read Data ------------------------------ */


	// Reads data from input, sends to solution class.
	private static DataTuple readData() throws FileNotFoundException {
		int nbrNodes = 0;
		int nbrEdges = 0;
		int capacity = 0;
		int nbrRoutes = 0;  // Ta bort så många som möjligt, behöver ej ta bort alla och är ej prioriterade.
		ArrayList<Edge> edges = new ArrayList<>();
		int[] removeEdges = null;
	
		File file = new File("data/secret/1small.in");

		try {
			Scanner scanner = new Scanner(file);
			nbrNodes = scanner.nextInt();
			nbrEdges = scanner.nextInt();
			capacity = scanner.nextInt();
			nbrRoutes = scanner.nextInt();

			int [] removEdges = new int[1 + nbrRoutes];

			for (int i = 0; i < nbrEdges; i++) {
				int n1 = scanner.nextInt();
				int n2 = scanner.nextInt();
				int c = scanner.nextInt();

				edges.add(new Edge(n1, n2, c));
			}
			
			// Reversed Routes list to ensure right edges gets deleted after finding the max flow.
			for (int i = nbrRoutes; i > 0; i--){
				int r = scanner.nextInt();
				removEdges[i] = r;
			}
			
			removeEdges = removEdges;

			scanner.close();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		DataTuple dataTuple = new DataTuple(edges, removeEdges, nbrNodes, nbrEdges, capacity, nbrRoutes);
		return dataTuple;

	}
	
/* ------------------------------ Nested class used for storing data ------------------------------ */


	// Used to contain multiple types of data.
	static class DataTuple{
		ArrayList<Edge> edges = new ArrayList<>();
		int[] removeEdges;
		int nbrNodes;
		int nbrEdges;
		int capacity;
		int nbrRoutes;
		
		public DataTuple(ArrayList<Edge> edges, int[] removeEdges, int nbrNodes, int nbrEdges, int capacity, int nbrRoutes) {
			this.edges = edges;
			this.removeEdges = removeEdges;
			this.nbrNodes = nbrNodes;
			this.nbrEdges = nbrEdges;
			this.capacity = capacity;
			this.nbrRoutes = nbrRoutes;
		}
		
	}

/* ------------------------------ Creates a solver ------------------------------ */


	  /**
	   * Creates an instance of a flow network solver. Use the {@link #addEdge(int, int, int)} method to
	   * add edges to the graph.
	   *
	   * @param n - The number of nodes in the graph including source and sink nodes.
	   * @param s - The index of the source node
	   * @param t - The index of the sink node
	  */
	  public FordFulkersonDfs(int n, int s, int t) {
	    	super(n, s, t);
	  }
	
	  // Performs the Ford-Fulkerson method applying a depth first search as
	  // a means of finding an augmenting path.
	  @Override
	  public void solve() {
	
	    	// Find max flow by adding all augmenting path flows.
	    	for (long f = dfs(s, INF); f != 0; f = dfs(s, INF)) {
			//List of connected edges update flow?
	      		markAllNodesAsUnvisited();
	      		maxFlow += f;
	    	}
	
	   }
	
	  // Removes edges specified in the removeEdges list.
	  @Override
	  public void getRemovableEdges() {
	
	    	// Find max flow by adding all augmenting path flows.
	    	for (long f = dfs(s, INF); f != 0; f = dfs(s, INF)) {
			//List of connected edges update flow?
	      		markAllNodesAsUnvisited();
	      		maxFlow += f;
	    	}
	  }
	
/* ------------------------------ Algorithm ------------------------------ */


	   private long dfs(int node, long flow) {
	   	// At sink node, return augmented path flow.
	    	if (node == t) 
	    		return flow;
			
		// List of edges connected to node. 
	    	List<Edge> edges = graph[node];
	    	visit(node);
	
	    	for (Edge edge : edges) {
	      		long rcap = edge.remainingCapacity();
	      		if (rcap >= 0 && !visited(edge.to)) {
				// Find max flow from source to sink
	        		long bottleNeck = dfs(edge.to, min(flow, rcap));

	        		// Augment flow with bottle neck value for edge and residual 
	        		if (bottleNeck > 0) {
	          			edge.augment(bottleNeck);
	          			return bottleNeck;
	        		}
	      		}
	    	}
	    	return 0;
	  }

}
