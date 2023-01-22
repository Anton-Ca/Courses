import java.util.ArrayList;
import java.util.Collection;

public class Node <E> {

    E value;
    ArrayList<Node<E>> neighbours = new ArrayList();
    int distance = 0;
    boolean visited = false;
    Node<E> parent;

    Node(E value) {
        this.value = value;
    }
    Node(E value, int distance)
    {
        this.value=value;
        this.distance =distance;
    }
    Node(Node<E> other)
    {
        this.value = other.value;
        this.distance=other.distance;
        this.neighbours = other.neighbours;
        this.parent = other=parent;
        this.visited = other.visited;

    }

    void addNeighbour(E value) {
        Node<E> add = new Node(value);
        neighbours.add(add);
    }

    void addNeighbour(Node n)
    {
        this.neighbours.add(n);
    }

    void addNeighbourdDistance (E value)
    {
        Node<E> add= new Node(value);
        add.distance=distance+1;
        add.parent = this;
        neighbours.add(add);
    }

    void addAllNeighbours(Collection<E> c)
    {
        for(E element : c)
            addNeighbour(element);
    }
    void addAllNeighboursDistance(Collection<E> c)
    {
        for(E element : c)
            addNeighbourdDistance(element);
    }

    @Override
    public int hashCode() {
        return value.hashCode();
    }

    @Override
    public boolean equals(Object other) {
        //This is a somewhat dirty solution
        if (other instanceof Node)
            return value.equals(((Node<E>) other).value);
        else
            return false;
    }
    @Override
    public String toString ()
    {
        return value.toString() + distance;
    }
    public String followParent()
    {
        if(parent!=null)
            return  parent.followParent() + " -> " + value.toString() ;
        return value.toString();
    }
}
