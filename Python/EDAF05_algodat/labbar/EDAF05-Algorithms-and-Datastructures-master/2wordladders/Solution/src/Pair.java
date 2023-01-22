public class Pair<E,V> {
    E first;
    V second;

    Pair (E first, V second)
    {
        this.first=first;
        this.second=second;
    }
    @Override
    public String toString()
    {
        return first.toString() + " " + second.toString();
    }
}
