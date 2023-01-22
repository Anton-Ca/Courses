import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Comparator;

public class run3 {

	public static void main(String[] args) throws FileNotFoundException {

		ArrayList<Point> points = readData();
		solution4 s = new solution4(points);

	}

	// Reads data from input, sends to solution class.
	private static ArrayList<Point> readData() throws FileNotFoundException {
		ArrayList<Point> points = new ArrayList<>();
		File file = new File("data/secret/6huger.in");
		
		try {
			Scanner scanner = new Scanner(file);
			int nbrOfPoints = scanner.nextInt();
			
			for(int i = 0; i < nbrOfPoints; i++){

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
