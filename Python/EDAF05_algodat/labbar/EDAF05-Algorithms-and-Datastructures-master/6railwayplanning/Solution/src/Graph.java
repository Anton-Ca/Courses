import java.util.*;

public class Graph<E extends Comparable<E>>
{

    public class Edge<E extends Comparable<E>> implements Comparable<Edge<E>>
    {
        int weight;
        int flow;
        Vertex<E> first;
        Vertex<E> second;
        Edge<E> reverse;
        public Edge (Vertex<E> first, Vertex<E> second, int weigth)
        {
            this.weight = weigth;
            this.first = first;
            this.second = second;
            this.flow = 0;
            reverse = null;
        }

        public Edge<E> setReverse (Edge<E> other)
        {
            reverse = other;
            return this;
        }

        public Vertex<E> getOther(E other)
        {
            if(first.value.compareTo(other) ==0)
            {
                return second;
            }
            return first;
        }

        @Override
        public int compareTo(Edge<E> e) {
            return weight - e.weight;
        }

        public boolean equals(Edge <E> other)
        {
                return other.first.compareTo(first) == 0 && other.second.compareTo(second) == 0&& other.weight == weight;
        }
        public int flowCapacity()
        {
            return weight-flow;
        }
        public void updateFlow (int flow)
        {
            this.flow += flow;
            reverse.flow = -this.flow;
        }
    }

    public class Vertex<E extends Comparable<E>> implements Comparable<Vertex<E>>{
        E value;
        Map<E,Edge<E>> edges;
        boolean isVisited;
        public Vertex (E value)
        {
            this.value = value;
            this.edges = new HashMap<>();
            this.isVisited = false;
        }
        public void addEdge (Vertex<E> other, int weight, boolean directional)
        {
            Edge newEdge = new Edge(this, other, weight);
            this.edges.put(other.value,newEdge);
        }
        public void addEdge(Edge<E> other)
        {
            edges.put(other.second.value, other);
        }
        @Override
        public int compareTo(Vertex<E> eVertex) {
            return this.value.compareTo(eVertex.value);
        }

        public Edge<E> edgeTo(E destination)
        {
            return edges.get(destination);
        }

        boolean isVisited ()
        {
            return isVisited;
        }
        void visit ()
        {
            isVisited = true;
        }
        void unvisit()
        {
            isVisited = false;
        }
    }
    Map<E,Vertex<E>> vertices;
    int nbrNodes;
    int totalWeigth;
    int nbrVisited;
    public Graph()
    {
        vertices= new HashMap<E, Vertex<E>>();
        nbrNodes = 0;
        totalWeigth = 0;
        nbrVisited = 0;
    }
    public void addVertex(E value)
    {
        this.vertices.put(value, new Vertex<E>(value));
        ++ nbrNodes;
    }
    public void addEdge (E first, E second, int weigth)
    {
        //we make sure the vertices actually exist, this way you can also build a graph
        //with only the information about the edges
        if(!vertices.containsKey(first))
            addVertex(first);
        if(!vertices.containsKey(second))
            addVertex(second);
        Edge<E> newEdge1 = new Edge(vertices.get(first),vertices.get(second),weigth);
        Edge<E> newEdge2 = new Edge(vertices.get(second),vertices.get(first),weigth);
        vertices.get(first).addEdge(newEdge1.setReverse(newEdge2));
        vertices.get(second).addEdge(newEdge2.setReverse(newEdge1));
        totalWeigth += weigth;
    }
    public Vertex<E> getAny()
    {
        return vertices.get(vertices.keySet().toArray()[0]);
    }
    public boolean containsVertex(E vertex)
    {
        return vertices.containsKey(vertex);
    }
    public Vertex<E> getVertex (E value)
    {
        return vertices.get(value);
    }
    public void visitVertex(E value)
    {
        if(!vertices.get(value).isVisited) {
            vertices.get(value).visit();
            nbrVisited++;
        }
    }
    public boolean allVisited()
    {
        return nbrVisited>= nbrNodes;
    }

    public void unvisitAll()
    {
        for(E key : vertices.keySet())
        {
            vertices.get(key).unvisit();
        }
    }
    public void removeEdge(E first, E second, int weight)
    {
        Map<E, Edge<E>> edges = vertices.get(first).edges;

        for(E val: edges.keySet())
        {
            if(edges.get(val).equals(new Edge<E>(vertices.get(first), vertices.get(second), weight)))
            {
                edges.get(val).reverse.first.edges.remove(val);
                edges.remove(val);
                break;
            }
        }
    }
    public int length()
    {
        return vertices.size();
    }

    public void removeFlow()
    {
        for(E val : vertices.keySet())
            for(E edgeVal: vertices.get(val).edges.keySet())
                vertices.get(val).edges.get(edgeVal).flow= 0;
    }
}