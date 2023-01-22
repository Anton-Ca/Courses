import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class DoubleMergeSort <E> {

    public Pair<List<E>> doubleSort(List<E> data, Comparator<E> comp1, Comparator<E> comp2)
    {
        if(data.size()<=1)
        {
            return new Pair<List<E>>(new ArrayList<>(data), new ArrayList<>(data));
        }
       Pair<List<E>> left;
       Pair<List<E>> right;

       left = doubleSort(data.subList(0,data.size()/2), comp1, comp2);
       right = doubleSort(data.subList((data.size()/2), data.size()), comp1, comp2 );
       return doubleMerge(left, right, comp1, comp2);
    }

    private Pair<List<E>> doubleMerge (Pair<List<E>> left, Pair<List<E>> right, Comparator<E> comp1, Comparator<E> comp2)
    {

        Pair<List<E>> result = new Pair<>(new ArrayList<>(), new ArrayList<>());
        while(!left.first.isEmpty() && !right.first.isEmpty())
        {
            if(comp1.compare(left.first.get(0), right.first.get(0))<=0) result.first.add(left.first.remove(0));
            else if(comp1.compare(left.first.get(0),right.first.get(0))>0) result.first.add(right.first.remove(0));

        }

        while (!left.second.isEmpty() && !right.second.isEmpty())
        {
            if (comp2.compare(left.second.get(0), right.second.get(0)) <= 0) result.second.add(left.second.remove(0));
            else if (comp2.compare(left.second.get(0), right.second.get(0)) > 0) result.second.add(right.second.remove(0));
        }
        while(!left.first.isEmpty()) result.first.add(left.first.remove(0));
        while(!left.second.isEmpty()) result.second.add(left.second.remove(0));
        while(!right.first.isEmpty()) result.first.add(right.first.remove(0));
        while(!right.second.isEmpty()) result.second.add(right.second.remove(0));

        return result;
    }
}
