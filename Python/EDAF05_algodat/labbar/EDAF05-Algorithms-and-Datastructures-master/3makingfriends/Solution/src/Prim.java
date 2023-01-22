import org.w3c.dom.Node;

import java.util.*;

public class Prim<E extends Comparable<E>>
{
    Graph<E> Prim (Graph<E> graph)
    {
        Graph<E> result = new Graph();

        PriorityQueue<Graph<E>.Edge<E>> edgeQueue = new PriorityQueue();
        Set<Graph<E>.Vertex<E>> vertexSet = new HashSet();

        Graph<E>.Vertex<E> currentVertex = graph.getAny();
        graph.visitVertex(currentVertex.value);

        while (!graph.allVisited())
        {
            for(Graph<E>.Edge<E> edge: currentVertex.edges)
            {
                if(!edge.second.isVisited())
                    edgeQueue.add(edge);
            }
            Graph<E>.Edge<E> cheapest = edgeQueue.poll();
            while (cheapest.second.isVisited())
            {
                cheapest=edgeQueue.poll();
            }
            result.addEdge(cheapest.first.value, cheapest.second.value, cheapest.weight);
            currentVertex = cheapest.second;
            graph.visitVertex(currentVertex.value);
        }

        return result;
    }

    //A Debug Mehtod
    public static Graph<Integer>.Edge<Integer> smallestInQue (Queue<Graph<Integer>.Edge<Integer>> queue)
    {
        Graph<Integer>.Edge<Integer> smallest = queue.peek();
        for(Graph<Integer>.Edge<Integer> e : queue)
        {
            if(e.compareTo(smallest)<0)
            {
                smallest = e;
            }
        }
        return smallest;
    }
}
