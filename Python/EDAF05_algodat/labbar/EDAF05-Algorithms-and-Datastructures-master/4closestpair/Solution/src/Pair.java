public class Pair <E>{
    E first;
    E second;

    public Pair (E first, E second)
    {
        this.first = first;
        this.second = second;
    }

    @Override
    public String toString()
    {
        return "(" + first.toString() + second.toString() + ")";
    }
}
