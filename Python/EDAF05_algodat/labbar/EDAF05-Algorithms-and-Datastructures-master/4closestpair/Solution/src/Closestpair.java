import java.sql.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class Closestpair {

    public Pair<Point> closestPair(List<Point> pointList)
    {
        List<Point> sortedX = new ArrayList<>();
        sortedX.addAll(pointList);
        sortedX.sort(new Comparator<Point>() {
            @Override
            public int compare(Point point, Point t1) {
                if(point.x == t1.x)
                    return point.y-t1.y;
                else return  point.x-t1.x;
            }
        });

        List<Point> sortedY = new ArrayList<>();
        sortedY.addAll(pointList);
        sortedY.sort(new Comparator<Point>() {
            @Override
            public int compare(Point point, Point t1) {
                return point.y-t1.y;
            }
        });
        return closest(sortedX, sortedY);
    }

    private Pair<Point> bruteForce (List<Point> px)
    {
        Pair<Point> min = new Pair<>(px.get(0),px.get(1));
        for(int i = 0; i<px.size(); ++i)
            for (int j = i+1; j<px.size(); ++j)
                if(px.get(i).distanceTo(px.get(j))<min.first.distanceTo(min.second)){ min = new Pair<>(px.get(i),px.get(j));}
        return min;
    }

    private Pair<Point> closest (List<Point> px, List<Point> py)
    {
        //Om vi har 3 eller mindre punkter kan vi bruteforca
        if(px.size() <= 3)
        {
            return bruteForce(px);
        }

        //Vi delar px och py upp i sublister
        List<Point> lx = px.subList(0, px.size()/2);
        List<Point> rx = px.subList(px.size()/2, px.size());

        List<Point> ly = /*py.subList(0,py.size()/2);*/ new ArrayList<>();
        List<Point> ry = /*py.subList(py.size()/2, py.size());*/ new ArrayList<>();

        List<Point> newPy = new ArrayList<>();

       for(int i = 0; i< py.size(); ++i)
       {
           if(py.get(i).y-rx.get(0).y < 0) {ly.add(py.get(i)); }
           else if(py.get(i).x-rx.get(0).x == 0)
           {
               if(py.get(i).y-rx.get(0).y < 0) { ly.add(py.get(i)); }
               else ry.add(py.get(i));
           }
           else ry.add(py.get(i));
       }

        Pair<Point> left = closest(lx, ly);
        Pair<Point> right = closest(rx, ry);


        Pair<Point> delta = left;
        if(left.first.distanceTo(left.second)>right.first.distanceTo(right.second))
            delta = right;

        //List<Integer> ks = new ArrayList<>();

        //denna kommer köra max 6 gånger
        for(int i = 0; i< py.size(); ++i)
        {
            int k = 0;
            for (int j = i+1; j< py.size() && j< i+6; ++j)
            {
                ++k;
                if(py.get(i).distanceTo(py.get(j))<delta.first.distanceTo(delta.second))
                {
                   // System.out.println(i + " " + j + py);
                    delta = new Pair<>(py.get(i), py.get(j));
                }
            }
           //ks.add(k);
        }

        return delta;

    }
}
