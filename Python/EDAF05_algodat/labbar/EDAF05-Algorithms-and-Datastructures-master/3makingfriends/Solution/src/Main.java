import java.util.Scanner;

public class Main {

    public static void main(String [] args)
    {
        Scanner scan = new Scanner(System.in);
        int nbrNodes = scan.nextInt();
        int nbrEdges = scan.nextInt();

        Graph<Integer> g = new Graph();
        for(int i=0; i<nbrEdges; ++i)
        {
            g.addEdge(scan.nextInt(),scan.nextInt(), scan.nextInt());
        }
        Prim p = new Prim();
        System.out.println(p.Prim(g).totalWeigth);
    }
}
