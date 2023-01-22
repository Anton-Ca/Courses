package textproc;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayList;

public class Holgersson {

	public static final String[] REGIONS = { "blekinge", "bohuslän", "dalarna", "dalsland", "gotland", "gästrikland",
			"halland", "hälsingland", "härjedalen", "jämtland", "lappland", "medelpad", "närke", "skåne", "småland",
			"södermanland", "uppland", "värmland", "västerbotten", "västergötland", "västmanland", "ångermanland",
			"öland", "östergötland" };

	public static void main(String[] args) throws FileNotFoundException {
		
		TextProcessor p1 = new SingleWordCounter("nils");
		TextProcessor p2 = new SingleWordCounter("norge");
		ArrayList<TextProcessor> A = new ArrayList<TextProcessor>();  
		A.add(p1);
		A.add(p2);
		Scanner s = new Scanner(new File("nilsholg.txt"));
		s.findWithinHorizon("\uFEFF", 1);
		s.useDelimiter("(\\s|,|\\.|:|;|!|\\?|'|\\\")+"); // se handledning

		while (s.hasNext()) {
			String word = s.next().toLowerCase();
			
			for (TextProcessor P : A){
				P.process(word);
			}
			//p1.process(word);
			//p2.process(word);

		}

		s.close();
		for (TextProcessor P : A){
			P.report(); 
		}
		//p1.report();
		//p2.report();
	}
}
