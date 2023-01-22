import java.util.*;

public class Graph <E>{
    Map<E,Node<E>> nodes = new HashMap();
    Graph(){}
    public void addValue(E value)
    {
        nodes.put(value, new Node<E>(value));
    }
    public Node<E> getNode(E value)
    {
        return nodes.get(value);
    }
    public void addAllValues(Collection<E> Value)
    {
        for(E e: Value)
            addValue(e);
    }
    public void addVertex(E current, E other)
    {
        if(nodes.get(current)==null)
            nodes.put(current,new Node<E>(current));
        if(nodes.get(other)==null)
            nodes.put(other, new Node<E>(other));
        nodes.get(current).addNeighbour(nodes.get(other));
    }
    public void addAllvertes(E current, Collection<E> others)
    {
        for(E e : others)
        {
            addVertex(current, e);
        }
    }

    @Override
    public String toString()
    {
        StringBuilder s = new StringBuilder();
        for(E e : nodes.keySet())
        {
           s.append(e+":" +nodes.get(e).neighbours +"\n");
        }
        return s.toString();
    }

    private void clearForBFS()
    {
        for(E e : nodes.keySet())
        {
            nodes.get(e).parent=null;
            nodes.get(e).distance = -1;
            nodes.get(e).visited = false;
        }
    }
    public int BFS(E start,E end)
    {
        if(start.equals(end))
            return 0;
        clearForBFS();
        Queue<Node<E>> q = new ArrayDeque();
        q.add(nodes.get(start));
        nodes.get(start).visited=true;
        nodes.get(start).distance=0;

        while (!q.isEmpty())
        {
            Node<E> current = q.poll();

            for(Node n : current.neighbours)
            {
                if(!n.visited)
                {
                    q.add(n);
                    n.visited = true;
                    n.parent = current;
                    n.distance = current.distance+1;
                    if(n.value.equals(end))
                        return n.distance;
                }
            }
        }
        return nodes.get(end).distance;
    }
}
