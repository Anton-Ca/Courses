import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Autori {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader (new InputStreamReader(System.in));	
		String str = br.readLine();
		String name = new String("");
		for (int i = 0; i < str.length(); i++) {
			Character c = str.charAt(i);
			if (Character.isUpperCase(c))
				name += c;
		}
		System.out.println(name);
	}
}