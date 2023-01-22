import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Scanner;

public class Main
{
    public static void main (String[] args) {

        Scanner scan = new Scanner(System.in);
        List<Point> points = new ArrayList<>();

        int nbrPoints = scan.nextInt();

        for(int i =0; i<nbrPoints; ++i) points.add(new Point(scan.nextInt(), scan.nextInt()));

        Pair<Point> shortesDistance = new Closestpair().closestPair(points);
        System.out.println(new DecimalFormat("0.000000").format(shortesDistance.first.distanceTo(shortesDistance.second)));
    }
}
