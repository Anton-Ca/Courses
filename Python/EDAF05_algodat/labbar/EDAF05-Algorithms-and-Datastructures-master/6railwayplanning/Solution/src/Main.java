import java.util.ArrayList;
import java.util.Scanner;

public class Main {

    public static void main (String [] args)
    {
        FordFulkerson<Integer> flowcalc = new FordFulkerson<>();
        Scanner scan = new Scanner(System.in);

        int nbrNodes = scan.nextInt();
        int nbrEdges = scan.nextInt();
        int nrbFlow = scan.nextInt();
        int nbrRoutes = scan.nextInt();

        Graph <Integer> g = new Graph<>();

        ArrayList<Tupple<Integer, Integer, Integer>> routes = new ArrayList<>();
        for(int i = 0; i < nbrEdges; ++i) {
            int first = scan.nextInt();
            int second = scan.nextInt();
            int weight = scan.nextInt();
            g.addEdge(first, second, weight);
            routes.add(new Tupple<>(first, second, weight));
        }

        int maxFlow = 0;
        int lastIndex = 0;
        for(int i = 1; i <= nbrRoutes; ++i)
        {
            int newFlow = flowcalc.maxFlow(g, 0,nbrNodes-1);
            lastIndex = i;
            maxFlow = newFlow;
            if(newFlow< nrbFlow)
                break;
            lastIndex = i;
            maxFlow = newFlow;
            Tupple<Integer, Integer, Integer> route = routes.get(scan.nextInt());
            g.removeEdge(route.first, route.second, route.third);
        }
        System.out.println(lastIndex +" " + maxFlow);
    }
}
