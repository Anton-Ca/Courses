import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public class run {

	public static void main(String[] args) throws FileNotFoundException {

		long a = System.currentTimeMillis();
		int points = readData();
		long b = System.currentTimeMillis();

		Arrays.sort(points, Comparator.comparingInt(p -> p.x));
		// System.out.println("TIME TO GATHER DATA: " + (b - a));

		solution3 s = new solution3(points);

	}

	// Reads data from input, sends to solution class.
	private static int readData() throws FileNotFoundException {
		int nodes = null;
		int edges = null;
		int capacity = null;
		int nbrRoutes = null;
		File file = new File("data/sample/1.in");
		
		try {
			Scanner scanner = new Scanner(file);
			nodes = new Point[scanner.nextInt()];
			edges = new Point[scanner.nextInt()];
			capacity = new Point[scanner.nextInt()];
			nbrRoutes = new Point[scanner.nextInt()];
			
			for (int i = 0; i < edges; i++) {

			
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		return points;
		
	}
	
