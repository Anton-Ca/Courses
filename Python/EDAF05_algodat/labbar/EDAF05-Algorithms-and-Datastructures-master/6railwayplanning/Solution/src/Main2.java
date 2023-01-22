import java.util.*;

public class Main2 {
    public static void main (String [] args)
    {
        FordFulgerson2 flowcalc = new FordFulgerson2();
        Scanner scan = new Scanner(System.in);

        int nbrNodes = scan.nextInt();
        int nbrEdges = scan.nextInt();
        int nrbFlow = scan.nextInt();
        int nbrRoutes = scan.nextInt();

        int nodes [][] = new int [nbrNodes][nbrNodes];
        Map<Integer, ArrayList<Integer>> neighbours = new HashMap<>();

        ArrayList<Tupple<Integer, Integer, Integer>> routes = new ArrayList<>();
        for(int i = 0; i < nbrEdges; ++i) {
            int first = scan.nextInt();
            int second = scan.nextInt();
            int weight = scan.nextInt();
           nodes[first][second] = weight;
           nodes[second][first] = weight;

           if(!neighbours.containsKey(first)) { neighbours.put(first,new ArrayList<>()); }
            neighbours.get(first).add(second);
           if(!neighbours.containsKey(second)) {neighbours.put(second,new ArrayList<>());}
            neighbours.get(second).add(first);

            routes.add(new Tupple<>(first, second, weight));
        }

        int maxFlow = 0;
        int lastIndex = 0;
        for(int i = 0; i < nbrRoutes; ++i)
        {
            int newFlow = flowcalc.FordFulgerson(nodes, 0,nbrNodes-1, nbrNodes, neighbours);
            if(newFlow< nrbFlow)
                break;
            lastIndex = i;
            maxFlow = newFlow;
            Tupple<Integer, Integer, Integer> route = routes.get(scan.nextInt());
            nodes[route.first][route.second] = 0;
            nodes[route.second][route.first] = 0;
        }
        System.out.println(lastIndex +" " + maxFlow);
    }
}
