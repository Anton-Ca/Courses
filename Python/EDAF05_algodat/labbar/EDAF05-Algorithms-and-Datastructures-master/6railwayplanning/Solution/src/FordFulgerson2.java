import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Map;
import java.util.Queue;

public class FordFulgerson2 {
    boolean bfs(int graph [][], int sink, int source, int parents[], int nbrNodes, Map<Integer, ArrayList<Integer>> neighbours)
    {
        boolean visited [] = new boolean[nbrNodes];

        Queue<Integer> q = new ArrayDeque<>();

        q.add(source);
        parents[source] = -1;
         while (!q.isEmpty())
         {
             int current = q.poll();

             for(int node : neighbours.get(current))
             {
                 if(!visited[node] && graph[current][node]>0)
                 {
                     q.add(node);
                     parents[node] = current;
                     visited[node] = true;
                     if(node == sink)
                         return visited[sink] == true;
                 }
             }
         }
         return visited[sink] == true;
    }

    public int FordFulgerson(int graph[][], int source, int sink, int nbrNodes, Map<Integer, ArrayList<Integer>> neigbhours)
    {
        int maxFlow = 0;
        int residuals [][] = new int [nbrNodes][nbrNodes];

        for(int x = 0; x<nbrNodes; ++x) for (int y =0; y<nbrNodes; ++y) residuals[x][y] = graph[x][y];

        int [] parents = new int[nbrNodes];

        while (bfs(residuals, sink, source, parents, nbrNodes, neigbhours))
        {
            int currentFlow = Integer.MAX_VALUE;

            for(int i = sink; i!=source; i = parents[i])
            {
                int node = parents[i];
                currentFlow = Math.min(currentFlow, residuals[node][i]);
            }

            for(int node=sink; node!=source; node=parents[node])
            {
                int parent = parents[node];
                residuals[parent][node] -= currentFlow;
                residuals[node][parent] += currentFlow;
            }
            maxFlow += currentFlow;
        }

        return maxFlow;
    }

}
