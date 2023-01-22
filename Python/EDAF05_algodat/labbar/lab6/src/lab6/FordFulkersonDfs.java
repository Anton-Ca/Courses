package lab6;

import static java.lang.Math.min;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class FordFulkersonDfs extends NetworkFlowSolver {
	
	public static void main(String[] args) throws FileNotFoundException {
		
		long a = System.currentTimeMillis();
		DataTuple data = readData();
		long b = System.currentTimeMillis();
		// System.out.println("TIME TO GATHER DATA: " + (b - a));
		
		int n = data.nbrNodes;
		int s = data.nbrNodes-2;
		int t = data.nbrNodes-1;

		FordFulkersonDfs solver;
	    solver = new FordFulkersonDfs(n, s, t);
	    
	    for (int i = 0; i < n; i++) {
	    	solver.addEdge(data.edges.get(i).from, data.edges.get(i).to, data.edges.get(i).capacity);
	    	
	    System.out.println(solver.getMaxFlow());
	    
	    System.out.println(solver.getGraph().length);
	    
	    }
	}

	// Reads data from input, sends to solution class.
	private static DataTuple readData() throws FileNotFoundException {
		int nbrNodes = 0;
		int nbrEdges = 0;
		int capacity = 0;
		int nbrRoutes = 0;  // Ta bort så många som möjligt, behöver ej ta bort alla och är ej prioriterade.
		ArrayList<Edge> edges = new ArrayList<>();
		
		File file = new File("data/sample/1.in");

		try {
			Scanner scanner = new Scanner(file);
			nbrNodes = scanner.nextInt();
			nbrEdges = scanner.nextInt();
			capacity = scanner.nextInt();
			nbrRoutes = scanner.nextInt();

			for (int i = 0; i < nbrEdges; i++) {
				int n1 = scanner.nextInt();
				int n2 = scanner.nextInt();
				int c = scanner.nextInt();

				edges.add(new Edge(n1, n2, c));
			}
			
			scanner.close();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		
		DataTuple dataTuple = new DataTuple(edges, nbrNodes, nbrEdges, capacity, nbrRoutes);
		
		return dataTuple;

	}
	
	// Used to contain multiple types of data.
	static class DataTuple{
		ArrayList<Edge> edges = new ArrayList<>();
		int nbrNodes;
		int nbrEdges;
		int capacity;
		int nbrRoutes;
		
		public DataTuple(ArrayList<Edge> edges, int nbrNodes, int nbrEdges, int capacity, int nbrRoutes) {
			this.edges = edges;
			this.nbrNodes = nbrNodes;
			this.nbrEdges = nbrEdges;
			this.capacity = capacity;
			this.nbrRoutes = nbrRoutes;
		}
		
	}

  /**
   * Creates an instance of a flow network solver. Use the {@link #addEdge(int, int, int)} method to
   * add edges to the graph.
   *
   * @param n - The number of nodes in the graph including source and sink nodes.
   * @param s - The index of the source node, 0 <= s < n
   * @param t - The index of the sink node, 0 <= t < n, t != s
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
      markAllNodesAsUnvisited();
      visitedToken++;
      maxFlow += f;
    }

    // Find min cut.
    for (int i = 0; i < n; i++) if (visited(i)) minCut[i] = true;
  }

  private long dfs(int node, long flow) {
    // At sink node, return augmented path flow.
    if (node == t) 
    	return flow;

    List<Edge> edges = graph[node];
    visit(node);

    for (Edge edge : edges) {
      long rcap = edge.remainingCapacity();
      if (rcap > 0 && !visited(edge.to)) {
        long bottleNeck = dfs(edge.to, min(flow, rcap));

        // Augment flow with bottle neck value
        if (bottleNeck > 0) {
          edge.augment(bottleNeck);
          return bottleNeck;
        }
      }
    }
    return 0;
  }

}