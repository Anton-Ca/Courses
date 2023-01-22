package textproc;
import java.util.ArrayList;
import java.util.Set;

public class SingleWordCounter implements TextProcessor {
        private String word;
        private int n;

        public SingleWordCounter(String word) {
                this.word = word;
                n = 0;
        }   

        public void process(ArrayList<String> w) {
//                if (w.equals(word)) { // equals istället för ==
//                        n++;
//                }   
        }   

        public void report() {
                System.out.println(word + ": " + n); 
        }   
    
}