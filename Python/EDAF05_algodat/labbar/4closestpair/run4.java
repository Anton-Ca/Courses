import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Comparator;

public class run4 {

	public static void main(String[] args) {

		ArrayList<Point> points = readData();
		solution4 s = new solution4(points);

	}

	// Reads data from input, sends to solution class.
	private static ArrayList<Point> readData(){
		ArrayList<Point> points = new ArrayList<>();
		
			Scanner scanner = new Scanner(System.in);
			int nbrOfPoints = scanner.nextInt();
			
			for(int i = 0; i < nbrOfPoints; i++){

				int coordX = scanner.nextInt();
				int coordY = scanner.nextInt();
			
				points.add(new Point(coordX, coordY));
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
