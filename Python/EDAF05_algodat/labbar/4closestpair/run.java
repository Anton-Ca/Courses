import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;

public class run {

	public static void main(String[] args) throws FileNotFoundException {

		long a = System.currentTimeMillis();
		ArrayList<Point> points = readData();
		long b = System.currentTimeMillis();

		// System.out.println("TIME TO GATHER DATA: " + (b - a));

		solution s = new solution(points);

	}

	// Reads data from input, sends to solution class.
	private static ArrayList<Point> readData() throws FileNotFoundException {
		ArrayList<Point> points = null;
		File file = new File("data/sample/1.in");
		
		try {
			Scanner scanner = new Scanner(file);

			points = new ArrayList<>(scanner.nextInt());
			
			while (scanner.hasNext()) {

			int coordX = scanner.nextInt();
			int coordY = scanner.nextInt();
			
			points.add(new Point(coordX, coordY));

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
			return " (" + x + ", " + y + ") ";
		}
	}
	
}
