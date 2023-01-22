import org.w3c.dom.Node;

import java.util.*;

public class FordFulkerson <E extends Comparable<E>>{

    public int maxFlow (Graph<E> graph, E source, E sink)
    {
        int maxFlow = 0;

        graph.removeFlow();

        Pair<Boolean, Map<E,E>> bfsResult = bfs(graph, source, sink);
        while (bfsResult.first)
        {
            int currentFlow = Integer.MAX_VALUE;
            for(E vertex = graph.getVertex(sink).value; graph.getVertex(vertex)!=graph.getVertex(source); vertex=bfsResult.second.get(vertex))
            {
                E value = bfsResult.second.get(vertex);
                currentFlow = Math.min(currentFlow,graph.getVertex(value).edgeTo(vertex).flowCapacity());
            }

            for(E vertex = graph.getVertex(sink).value; graph.getVertex(vertex)!=graph.getVertex(source); vertex=bfsResult.second.get(vertex))
            {
                E parent = bfsResult.second.get(vertex);
                graph.getVertex(parent).edgeTo(vertex).updateFlow(currentFlow);
            }
            maxFlow+=currentFlow;
            bfsResult = bfs(graph, source, sink);
        }
        return maxFlow;
    }

    private Pair<Boolean,Map<E,E>> bfs(Graph<E> graph, E source, E sink)
    {
        graph.unvisitAll();
        Queue<Graph<E>.Vertex<E>> que = new ArrayDeque<>();
        Map<E,E> parents = new HashMap<>();

        que.add(graph.getVertex(source));
        graph.getVertex(source).visit();
        parents.put(source,null);

        while(que.size()>0 && !graph.getVertex(sink).isVisited())
        {
            Graph<E>.Vertex<E> polled = que.poll();
            for(E dest: polled.edges.keySet())
            {
                Graph<E>.Edge<E> currentEdge = polled.edges.get(dest);
                if(!currentEdge.second.isVisited() && currentEdge.flowCapacity()>0)
                {
                    que.add(currentEdge.second);
                    currentEdge.second.visit();
                    parents.put(currentEdge.second.value,polled.value);
                }
            }
        }
        return new Pair<>(graph.getVertex(sink).isVisited(),parents);
    }
}
