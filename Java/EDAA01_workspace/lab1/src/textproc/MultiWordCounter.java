package textproc;

import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class MultiWordCounter implements TextProcessor {

	private Map<String, Integer> m = new HashMap<String, Integer>();

	public MultiWordCounter(String[] landskap) {
		for (String str : landskap) {
			m.put(str, 0);
		}
	}

	public void process(ArrayList<String> w) {
//		if (m.containsKey(w)) {
			// Lägger till 1 om det inte finns någon map med motsvarande key, annars
			// summerar 1 till värdet. (Vi kollar ovan så det alltid finns en key)
//			m.merge(w, 1, Integer::sum);
//		}

	}

	public void report() {
		for (String key : m.keySet()) {
			System.out.println(key + ": " + m.get(key));
		}
	}

}
