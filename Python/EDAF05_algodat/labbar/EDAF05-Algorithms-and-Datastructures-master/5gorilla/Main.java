import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main
{
    public static void main (String [] args)
    {
        Scanner scan = new Scanner(System.in);

        String input = scan.next();
        List<Character> chars = new ArrayList<>();

        while(Character.isAlphabetic(input.charAt(0))) { chars.add(input.charAt(0)); input= scan.next(); }

        //Now we can create the cost Matrix
        int[][] costs = new int[chars.size()][chars.size()];

        //The next inputs  is the table of numbers we have chars.size() lines with chars.size() numbers
        for(int i = 0; i<chars.size(); ++i)
            for (int j = 0; j<chars.size(); ++j) {costs[i][j] = Integer.parseInt(input); input = scan.next();}

        //the next number is is an int with the amount of lines to read
        int nbrQueries = Integer.parseInt(input);

        char [] chars2 = new char[chars.size()];
        for(int i =0; i< chars.size(); ++i)
        {
            chars2[i] = chars.get(i);
        }

        SequenceAlign al = new SequenceAlign();
        for(int i = 0; i<nbrQueries; ++i)
        {
           Pair<String> sol =  al.align(new Pair<>(scan.next(), scan.next()),costs, -4, chars2,'*', true);

            System.out.println(sol.first  + " " + sol.second);
        }
    }
}

