import java.util.*;

public class solution {
    public static void main (String[] args){

        //reading from the console
        Scanner scan = new Scanner(System.in);

        //We read the number of people from the first line
        //TODO: If we run into errors, we change this to scan.nextInt(); (That makes reading to the linebreak superfluous)
        int nbrPeople = Integer.parseInt(scan.nextLine());

        //We instantiate the maps to hold the preferences for the men and women
        Map<Integer, List<Integer>> manPref = new HashMap<>();
        Map<Integer, List<Integer>> womPref = new HashMap<>();

        //Reading the preferences
        for(int i = 0; i< 2*nbrPeople; ++i)
        {
            /*
            We scan each next int (we read 2*nbrPeople lines that each contain nbrPeople+1
            numbers(personNumber and then the n ranked preferences))
            */
            int person = scan.nextInt()-1;
            List<Integer> prefs = new ArrayList<>();

            for(int b =0; b<nbrPeople; ++b)
            {
                /*
                we have a ranked list for all the men.
                This means that we add the next nbrPeople numbers into the list of preferences.
                */
                prefs.add(scan.nextInt()-1);
            }

            /*
            The woman line is first for a given index. This means if we have an entry for a
             women in the map, we put it int the map for the man preferences
            */
            if(womPref.containsKey(person))
            {
                //We have a woman entry, we now put it in the man preferences
                manPref.put(person, prefs);
            }
            else
            {
                //We don't have an entry in the women pref map. we map the list to the women.
                womPref.put(person, invert(prefs));
            }
        }

        //we can now get the array from the match method. This will also be what we print out later
        int[] matches = match(nbrPeople,manPref,womPref);

        for(int i=0; i<matches.length; ++i)
       {
           System.out.println(matches[i]+1);
       }
    }

    public static List<Integer> invert (List<Integer>base)
    {
        List<Integer> result= new ArrayList(base);
        for(int i=0; i<base.size(); ++i)
        {
            result.set(base.get(i), i);
        }
        return result;
    }

    /**
     * Matches the men and the women to a stable Matching
     * @param nbrMenAndWomen the number of men and women, This should be an even number as there are as much men and
     *                       women in the amount
     * @param manPrefs the map that contains the preferences for the men
     * @param womPrefs the map that contains the preferences for the women.
     * @return a one-dimensional int array (int[]) with the found matches
     */
    private static int[] match(int nbrMenAndWomen,Map<Integer, List<Integer>> manPrefs, Map<Integer, List<Integer>> womPrefs)
    {
        /*
        woman's partners
        We will also be returning this. This keeps track of the number of the man that the women has as a partner
        */
        int [] womPart = new int[nbrMenAndWomen];

        for(int i=0 ; i<nbrMenAndWomen ; ++i)
            womPart[i] = -1;
        /*
        The index in the prefList of man i that he proposed to last.
         This is so he can continue proposing to the next women, the next time he needs to propose in the loop.
        */
        int[] proposalIndex = new int [nbrMenAndWomen];

        boolean isSingle[] = new boolean [nbrMenAndWomen];

        int free = nbrMenAndWomen;


        Queue<Integer> singleMen = new ArrayDeque<>();
        for(int i = 0; i< nbrMenAndWomen; ++i)
            singleMen.add(i);

        //While there are singles
        while(!singleMen.isEmpty())
        {
            //Getting the first single man in the list
            int man = singleMen.poll();

            //Getting the mans preferences
            List<Integer> currentPrefs = manPrefs.get(man);

            /*
            we go through the list of preferences for the man. We start where we left of, the last time we looked
            at proposing for the given man. We also have to stop when the man gets a partner because then he stops looking
             We do not have a variable for the loop but rather we use the value stored in the proposalIndex array
            */
            for(; proposalIndex[man]<nbrMenAndWomen && !isSingle[man] ; ++proposalIndex[man])
            {
                //Going through all the women the man wants to "have"
                int woman = currentPrefs.get(proposalIndex[man]);

                //If the woman does not have a partner:
                if(womPart[woman] == -1) {
                    womPart[woman] = man;
                    isSingle[man] = true;
                }
                else {
                    //if the woman does have a partner:
                    int rival = womPart[woman];
                    if(!WomanPrefersCurrentPartner(womPrefs.get(woman), man,rival))
                    {
                        womPart[woman] = man;
                        isSingle[man] = true;
                        isSingle[rival] = false;
                        singleMen.add(rival);
                        break;
                    }
                }
            }
        }
        /*
        What we care about is the partners for the women. Because both the women and men are represented by
        numbers,we can use the index
        */
        return womPart;
    }

    /**
     * Checks if the woman prefers her current partner over the man proposing.
     * The CurrentPartner is the woman's current partner
     * @param womPrefs the list of preferences for the woman
     * @param man the number representing the man that proposes to the woman
     * @param CurrentPartner the number representing the woman's current partner
     * @return true if the woman prefers her current partner over the supplied man. Otherwise, false.
     */
    private static boolean WomanPrefersCurrentPartner(List<Integer> womPrefs, int man, int CurrentPartner)
    {
        if(womPrefs.get(man)>womPrefs.get(CurrentPartner))
            return true;
        return false;
    }
}