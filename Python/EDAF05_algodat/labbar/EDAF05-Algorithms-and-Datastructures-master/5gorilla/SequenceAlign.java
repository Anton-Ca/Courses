public class SequenceAlign {

    char [] charIndexes;
    int [][] costs;
    int costRemoved;
    char removedSymbol;

    AlignedPair [][] cache;

    public Pair<String> align (Pair<String> input, int [] [] costs, int costReplacement, char [] chars, char removedSymbol, boolean recursive)
    {
        this.costs = costs;
        this.costRemoved = costReplacement;
        this.removedSymbol = removedSymbol;
        this.charIndexes = chars;
        this.cache = new AlignedPair[input.first.length()][input.second.length()];
        Pair<String> result;
        if(recursive) {
            AlignedPair recResult =  opt(input,input.first.length()-1, input.second.length()-1);
            return new Pair<>(recResult.first, recResult.second);
        }
        else result = optItter(input);
        return result;

    }

   private Pair<String> optItter (Pair<String> input) {
       int[][] distance = new int[input.first.length() + 1][input.second.length() + 1];


       for (int i = 1; i < input.first.length() +1 ; ++i) { distance[i][0] = distance[i - 1][0] + costRemoved; }
       for (int j = 1; j < input.second.length() +1 ; ++j) { distance[0][j] = distance[0][j - 1] + costRemoved; }

       for (int i = 1; i < input.first.length() +1; ++i) {
           for (int j = 1; j < input.second.length() +1; ++j) {
               int both = distance[i - 1][j - 1] + costs[getCharIndex(input.first.charAt(i - 1))][getCharIndex(input.second.charAt(j - 1))];
               int first = distance[i - 1][j] + costRemoved;
               int second = distance[i][j - 1] + costRemoved;
               distance[i][j] = Math.max(both,Math.max(first,second));
           }
       }
       return traceback(input, distance);
   }
   private Pair<String> traceback (Pair<String> strings, int [][] distances)
   {
       int i = strings.first.length(), j = strings.second.length();

       Pair<String>  result = new Pair<String>("","");
       while (i>0 && j>0)
       {
           if(distances[i][j] - costs [getCharIndex(strings.first.charAt(i-1))][getCharIndex(strings.second.charAt(j-1))] == distances[i-1][j-1])
           { result = new Pair(strings.first.charAt(i-- -1)+result.first, strings.second.charAt(j-- -1) + result.second); }
           else if(distances[i][j] - costRemoved == distances[i][j-1])
           { result = new Pair(removedSymbol + result.first, strings.second.charAt(j-- - 1) + result.second); }
           else if(distances[i][j] - costRemoved == distances[i-1][j])
           { result = new Pair(strings.first.charAt(i-- - 1) + result.first, removedSymbol + result.second); }
           else
               { System.out.println("Something went wrong, didn't find a traceback case");result = new Pair(strings.first.charAt(i-- -1)+result.first, strings.second.charAt(j-- -1) + result.second); }
       }
       while (i>0) { result = new Pair<>(strings.first.charAt(i-- -1) + result.first, removedSymbol + result.second); }
       while (j>0) { result = new Pair<>(removedSymbol + result.first, strings.second.charAt(j-- -1) + result.second); }
       return result;


   }



    private AlignedPair opt(Pair<String> strings, int i, int j)
    {
        if(i>=0 && j>=0 && cache[i][j]!=null) {return new AlignedPair(cache[i][j]);}

        if(i < 0 && j <0) { return new AlignedPair(); }

        else if (i < 0) {
            AlignedPair retObj = new AlignedPair();
            while (j>=0) { retObj.update(removedSymbol, strings.second.charAt(j--)); }
            return retObj;
        }

        else if(j < 0){
            AlignedPair retObj = new AlignedPair();
            while (i>=0) { retObj.update(strings.first.charAt(i--),removedSymbol); }
            return retObj;
        }
        else {

            AlignedPair first = opt(strings, i-1, j).update(strings.first.charAt(i), removedSymbol);
            AlignedPair second = opt(strings, i, j - 1).update(removedSymbol, strings.second.charAt(j));
            AlignedPair same = opt(strings, i-1, j-1).update(strings.first.charAt(i), strings.second.charAt(j));

            if (first.score() > second.score() && first.score() > same.score()) {
                return cacheSolution(first, i,j);
            } else if (second.score() > first.score() && second.score() > same.score()) {
                return cacheSolution(second, i,j);
            } else {
                return cacheSolution(same, i ,j);
            }
        }
    }


    private AlignedPair getChached (int i, int j)
    {
        //we copy the value store in the cache if it exists
        if(i>=0 && j>=0 && cache[i][j]!=null) {return new AlignedPair(cache[i][j]);}
        return null;
    }

    private AlignedPair cacheSolution (AlignedPair input, int i, int j)
    {
        if(i>=0 && j>=0) {cache[i][j] = new AlignedPair(input); }
        return input;
    }

    private int getCharIndex (char a)
    {
            for (int i = 0; i < charIndexes.length; ++i) if (charIndexes[i] == a) return i;
            return -1;
    }

    public class AlignedPair{
        String first;
        String second;
        int cost;

        public AlignedPair ()
        {
            this.first = "";
            this.second = "";
            this.cost = 0;
        }

        /**
         * A copy constuctor to use in caching
         * @param other
         */
        public AlignedPair (AlignedPair other)
        {
            this.first = new String(other.first);
            this.second = new String(other.second);
            cost = other.cost;
        }

        public AlignedPair(String first, String second)
        {
            this.first = first;
            this.second = second;
        }

        public AlignedPair update (char c1, char c2)
        {
            first +=  c1;
            second += c2 ;

           if(c1 == removedSymbol || c2 == removedSymbol ) cost += costRemoved;
           else cost += costs[getCharIndex(c1)][getCharIndex(c2)];

           return this;
        }

        public int score() { return cost; }

        @Override
        public String toString() { return "(" + first + "," + second + ")"; }
    }
}

