import java.sql.Statement;
import java.util.*;

public class Solution {

    public static void main (String [] args)
    {
        Scanner scan = new Scanner(System.in);

        int numberWords = scan.nextInt();
        int numberQueries = scan.nextInt();

        List<String> wordList = new ArrayList();

        for(int i = 0; i<numberWords; ++i)
        {
            wordList.add(scan.next());
        }

        for(int i = 0; i<numberQueries; ++i)
        {
            String start = scan.next();
            String end = scan.next();

            int distance = BFG(wordList, start, end);

            System.out.println(distance==-1?"Impossible":distance);

        }

    }

    private static int BFG(List<String> dictionary, String start, String end)
    {
        Node<String> startNode = new Node(start);

        List<String> notVisited = new ArrayList();

        notVisited.addAll(dictionary);
        notVisited.remove(start);


        Queue<Node<String>> waitingNodes = new ArrayDeque();
        waitingNodes.add(startNode);


        while (!waitingNodes.isEmpty())
        {
            System.out.println(waitingNodes);
            Node<String> current = waitingNodes.poll();
            System.out.println(current);
            if(current.value.equals(end))
                return current.distance;

            List<String> neighbours = findNeighbours(notVisited,current.value);
            notVisited.removeAll(neighbours);
            current.addAllNeighboursDistance(neighbours);
            waitingNodes.addAll(current.neighbours);

        }
        return -1;
    }

    private static List<String> findNeighbours(List<String> needNeighbours, String current)
    {
        List<String> result = new ArrayList();
        for(String s : needNeighbours)
        {
            if(s!=current && (isNeighbour(current, s)||isBridge(current, s))) {
                result.add(s);
            }
        }
        return result;
    }

    private static boolean isNeighbour (String current, String other )
    {
        int distance = 0;
            for(int i = 0; i<current.length(); ++i)
            {
                if(current.charAt(i)!=other.charAt(i))
                    ++distance;
            }
            return distance==1;
    }
    private static boolean isBridge (String current, String other)
    {
        //of the last for letters of current are present in other
        //We get the last 4 letters of current and check if other contain all of them

        String last4 = current.substring(current.length()-4, current.length());
        ArrayList<Character> compare = new ArrayList();
        for(char c: other.toCharArray())
            compare.add(c);

        for(char c : last4.toCharArray()) {
            if (compare.indexOf(c) < 0)
                return false;
            compare.remove(compare.indexOf(c));
        }
        return true;
    }
}

