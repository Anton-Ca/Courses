import java.util.*;

public class Graph<E extends Comparable<E>>
{

    public class Edge<E extends Comparable<E>> implements Comparable<Edge<E>>
    {
        int weight;
        Vertex<E> first;
        Vertex<E> second;
        public Edge (Vertex<E> first, Vertex<E> second, int weigth)
        {
            this.weight = weigth;
            this.first = first;
            this.second = second;
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
    }

    public class Vertex<E extends Comparable<E>> implements Comparable<Vertex<E>>{
        E value;
        List<Edge> edges;
        boolean isVisited;
        public Vertex (E value)
        {
            this.value = value;
            this.edges = new ArrayList<Edge>();
            this.isVisited = false;
        }
        public void addEdge (Vertex<E> other, int weight, boolean directional)
        {
            Edge newEdge = new Edge(this, other, weight);
            this.edges.add(newEdge);
        }
        public void addEdge(Edge<E> other)
        {
            edges.add(other);
        }
        @Override
        public int compareTo(Vertex<E> eVertex) {
            return this.value.compareTo(eVertex.value);
        }

        boolean isVisited ()
        {
            return isVisited;
        }
        void visit ()
        {
            isVisited = true;
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
        vertices.get(first).addEdge(new Edge(vertices.get(first),vertices.get(second),weigth));
        vertices.get(second).addEdge(new Edge(vertices.get(second),vertices.get(first),weigth));
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
}
