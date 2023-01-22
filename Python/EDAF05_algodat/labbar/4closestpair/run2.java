import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public class run2 {

	public static void main(String[] args) throws FileNotFoundException {

		long a = System.currentTimeMillis();
		Point[] points = readData();
		long b = System.currentTimeMillis();

		Arrays.sort(points, Comparator.comparingInt(p -> p.x));
		// System.out.println("TIME TO GATHER DATA: " + (b - a));

		solution3 s = new solution3(points);

	}

	// Reads data from input, sends to solution class.
	private static Point[] readData() throws FileNotFoundException {
		Point[] points = null;
		File file = new File("data/secret/2med.in");
		
		try {
			Scanner scanner = new Scanner(file);
			points = new Point[scanner.nextInt()];
			int count = 0;
			
			while (scanner.hasNext()) {

			int coordX = scanner.nextInt();
			int coordY = scanner.nextInt();
			
			points[count++] = new Point(coordX, coordY);
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		return points;
		
	}
	
	static class Point {
		int x;
		int y;
		
		public Point (int x, int y) {
			this.x = x;
			this.y = y;
		}
		
		public int getX() {
			return x;
		}
		
		public int getY() {
			return y;
		}
		
		@Override
		public String toString() {
			return "\n" + x + " " + y;
		}
	}
	
}
