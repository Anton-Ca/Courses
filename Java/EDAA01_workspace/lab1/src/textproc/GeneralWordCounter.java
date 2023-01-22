package textproc;

import java.util.Map;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.TreeMap;
import java.util.ArrayList;
import java.util.List;

public class GeneralWordCounter implements TextProcessor {

	private Map<String, Integer> m = new TreeMap<String, Integer>();
	private Set<String> s = new HashSet<String>();
	
	Set<Map.Entry<String, Integer>> wordSet;
	List<Map.Entry<String, Integer>> wordList;

	public GeneralWordCounter(Set<String> stop) {
		for (String str : stop) {
			s.add(str);
		}

	}

	public void stopWords(Set<String> stopwords) {
	}

	/**
	 * for (String str : stopwords) { s.add(str); m.remove(str); } }
	 */
	public void process(ArrayList<String> w) {

		for (String str : w) {
			if (s.contains(str) == false) {
				if (m.containsKey(str)) {
					m.put(str, m.get(str) + 1);
				} else {
					m.put(str, 1);
				}
			}
		}

		// }
	}

	public List<Map.Entry<String, Integer>> getWordList(){
		wordSet = m.entrySet();
		wordList = new ArrayList<>(wordSet);
		wordList.sort(new WordCountComparator());
		return wordList;
	}

	
	
	public void report() {
		//wordSet = m.entrySet();
		//wordList = new ArrayList<>(wordSet);
		//getWordList().sort(new WordCountComparator());
		getWordList();
		
		for (int i = 0; i < 20; i++) {
			System.out.println(wordList.get(i));
		}

		/**
		 * for (String key : m.keySet()) { if (m.get(key) >= 200) {
		 * System.out.println(key + ": " + m.get(key)); } }
		 */
	}
}
