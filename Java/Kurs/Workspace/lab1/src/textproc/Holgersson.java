package textproc;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class Holgersson {

	public static final String[] REGIONS = { "blekinge", "bohuslän", "dalarna", "dalsland", "gotland", "gästrikland",
			"halland", "hälsingland", "härjedalen", "jämtland", "lappland", "medelpad", "närke", "skåne", "småland",
			"södermanland", "uppland", "värmland", "västerbotten", "västergötland", "västmanland", "ångermanland",
			"öland", "östergötland" };

	public static void main(String[] args) throws FileNotFoundException {
	//	Set<String> str = new HashSet<String>();	
		Set<String> w  = new HashSet<String>();

		TextProcessor Multi = new MultiWordCounter(Holgersson.REGIONS);

//		TextProcessor p1 = new SingleWordCounter("nils");
//		TextProcessor p2 = new SingleWordCounter("norge");
		ArrayList<TextProcessor> A = new ArrayList<TextProcessor>();  

	//	ArrayList<TextProcessor> AL = new ArrayList<TextProcessor>();  
//		A.add(p1);
//		A.add(p2);
		A.add(Multi);
		Scanner s = new Scanner(new File("nilsholg.txt"));
	//	Scanner scan = new Scanner(new File("undantagsord.txt"));
		s.findWithinHorizon("\uFEFF", 1);
		s.useDelimiter("(\\s|,|\\.|:|;|!|\\?|'|\\\")+"); // se handledning
/**		scan.findWithinHorizon("\uFEFF", 1);
		scan.useDelimiter("(\\s|-|\\.|:|;|!|\\?|'|\\\")+"); 
		
		TextProcessor stop  = new GeneralWordCounter(str);
		while (scan.hasNext()) {
			String word = scan.next().toLowerCase();
			str.add(word);
		}		
		stop.stopWords(str);
*/		while (s.hasNext()) {
			String word = s.next().toLowerCase();
			w.add(word); //Blir inte här ett problem med att TextProcessor all initieras innan och förblir tom?
		}	
			TextProcessor Gen  = new GeneralWordCounter(w);
			ArrayList<TextProcessor> AL = new ArrayList<TextProcessor>();
			AL.add(Gen);
			while (s.hasNext()) {
			String word = s.next().toLowerCase();
			
			for (TextProcessor P : AL){
				P.process(word);
			}
			/**while (s.hasNext()) {
			String word = s.next().toLowerCase();
			
			for (TextProcessor P : A){
				P.process(word);
			}*/
			// p1 & p2 
			//p1.process(word);
			//p2.process(word);
		}

		s.close();
/**		scan.close();
		Multi.report();
*/		
		
		Gen.report();		
		for (TextProcessor P : AL){
			P.report(); 
		}
		//p1.report();
		//p2.report();
	}
}
