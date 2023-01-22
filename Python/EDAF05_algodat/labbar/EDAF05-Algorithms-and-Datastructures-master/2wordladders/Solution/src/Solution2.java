import javax.management.Query;
import java.util.*;

public class Solution2 {

    public static void main (String [] args)
    {

        Scanner scan = new Scanner(System.in);

        int numberWords = scan.nextInt();
        int numberQueries = scan.nextInt();

        List<String> wordList = new ArrayList();

        for(int i = 0; i<numberWords; ++i)
        {
            wordList.add(scan.next().trim().toLowerCase());
        }

        Graph<String> g = new Graph();
        g.addAllValues(wordList);
        for(String s : wordList)
        {
            Collection<String> c = findNeighbours(wordList,s);
            g.addAllvertes(s, c);
        }

        for(int i = 0; i<numberQueries; ++i)
        {
            String start = scan.next().trim().toLowerCase();
            String end = scan.next().trim().toLowerCase();
            int distance = g.BFS(start, end);
            if(distance>=0)
                System.out.println(g.BFS(start, end));
            else
                System.out.println("Impossible");
        }
    }

    private static List<String> findNeighbours(List<String> needNeighbours, String current)
    {
        List<String> result = new ArrayList();
        for(String s : needNeighbours)
        {
            if(!s.equals(current) && (isBridge(current, s)))
                result.add(s);
        }
        return result;
    }
    private static boolean isBridge (String current, String other )
    {
        //of the last for letters of current are present in other
        //We get the last 4 letters of current and check if other contain all of them

        String last4 = current.substring(current.length()-4);
        ArrayList<Character> compare = new ArrayList();
        for(char c: other.toCharArray())
            compare.add(c);

        for(char c : last4.toCharArray()) {
            if (compare.indexOf(c) < 0)
                return false;
            compare.remove(compare.indexOf(c));
        }
        return compare.size() == other.length()-4;
    }
}

