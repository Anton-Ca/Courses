package textproc;
import java.util.Map;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.ArrayList;

public class GeneralWordCounter implements TextProcessor {

        private Map<String ,Integer> m = new HashMap<String, Integer>(); 
	private Set<String> s = new HashSet<String>();

        public GeneralWordCounter(Set<String> landskap) {
		for (String str : landskap){
			m.put(str, 0);
		}
	}       

         public void stopWords(Set<String> stopwords) {
		for (String str : stopwords) {
			s.add(str);
		}
	}

        public void process(String w) {
			if (s.contains(w) == false){
				if(m.containsKey(w)){
                			m.put(w, m.get(w) +1);
				} 
			} else {
				return; 
			}
        }
                
	public void report() {
		for(String key : m.keySet()){
			if (m.get(key) >= 200){
				System.out.println(key + ": " + m.get(key));
			}
		}       
	}       
}