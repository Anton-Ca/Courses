package lab4;

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
		ArrayList<Point> points = readData();
		long b = System.currentTimeMillis();

		points.sort(Comparator.comparingInt(p -> p.x));
		// System.out.println("TIME TO GATHER DATA: " + (b - a));

		solution2 s = new solution2(points);

	}

	// Reads data from input, sends to solution class.
	private static ArrayList<Point> readData() throws FileNotFoundException {
		ArrayList<Point> points = null;
		File file = new File("lab4/src/lab4/data/sample/1.in");
		
		try {
			Scanner scanner = new Scanner(file);
			int count = 0;
			
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
		int i = 0;
		
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