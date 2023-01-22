import java.util.*;

public class solution {
	private ArrayList<run.Point> points;
	private ArrayList<run.Point> sortedPoints;

	public solution(ArrayList<run.Point> points) {
		this.points = points;
		sortedPoints = null;

		long a = System.currentTimeMillis();
		sortedPoints = mergeSort(points);
		long b = System.currentTimeMillis();
		// System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");

		a = System.currentTimeMillis();
		//System.out.println(findClosestPair(sortedPoints));
		b = System.currentTimeMillis();
		// System.out.println("TIME TO EXECUTE ALGORITHM: " + (b - a) + "\n");
		System.out.println("SIZE = " + sortedPoints.size() + " POINTS: " + sortedPoints.toString());
	}
	
	// Sorting

	public ArrayList<run.Point> mergeSort(ArrayList<run.Point> points) {
		ArrayList<run.Point> tmpArray = new ArrayList<>(points.size());
		return sort(points, tmpArray, 0, points.size()); // Add size() -1 if nullPointer
	}

	private ArrayList<run.Point> sort(ArrayList<run.Point> points, ArrayList<run.Point> tmpArray, int first, int last ) {
		if (first < last) {
			int mid = (first + last) / 2;
			sort(points, tmpArray, first, mid);
			sort(points, tmpArray, mid + 1, last);
			return merge(points, tmpArray, first, mid + 1, last);
		}
		return null;
	}
		
	@SuppressWarnings({ "unchecked", "rawtypes" })
	private ArrayList<run.Point> merge(ArrayList<run.Point> points, ArrayList<run.Point> tmpArray, int leftPos, int rightPos, int rightEnd) {
			int leftEnd = rightPos - 1;
			int tmpPos = leftPos;
			int leftStart = leftPos;
			while(leftPos <= leftEnd && rightPos <= rightEnd) {
				if (((Comparable) points.get(leftPos).x).compareTo(points.get(rightPos).x) <= 0) {
					//tmpArray.get(tmpPos++) = points.get(leftPos++);
					tmpArray.add(points.get(leftPos++));
				} else {
					//tmpArray.get(tmpPos++) = points.get(rightPos++);
					tmpArray.add(points.get(rightPos++));
				}
			}
			while (leftPos <= leftEnd) {
				//tmpArray.get(tmpPos++) = points.get(leftPos++);
				tmpArray.add(points.get(leftPos++));
			}
			while (rightPos <= rightEnd) {
				//tmpArray.get(tmpPos++) = points.get(rightPos++);
				tmpArray.add(points.get(rightPos++));
			}
			for (int i = leftStart; i <= rightEnd; i++) {
				//points.get(i) = tmpArray.get(i);
				points.add(tmpArray.get(i));
			}
			return points;
		}
	

	// Algorithm
	
	public float findClosestPair(ArrayList<run.Point> sortedPoints) {
		ArrayList<run.Point> sP = sortedPoints;
		int length = sP.size();
		
		if (length < 4)
			return bruteForce(length).distance();
		
		ArrayList<run.Point> left = new ArrayList<>(sortedPoints.size()/2);
		ArrayList<run.Point> right = new ArrayList<>(sortedPoints.size()/2);
		
		for (int i = 0; i < sortedPoints.size(); i++) {
			
			if (i < sortedPoints.size()/2)
				left.add(sortedPoints.get(i));
			
			if (i > sortedPoints.size()/2)
				right.add(sortedPoints.get(i));
		}
			
			float distanceLeft = findClosestPair(left);
			float distanceRight = findClosestPair(right);
			float distanceBoth = Integer.MAX_VALUE;

			if (distanceLeft > distanceRight) 
				distanceBoth = distanceRight;
			else
				distanceBoth = distanceLeft;
			
			
			
		return 0;
	}
	
	public Pair bruteForce(int length) {
		float closestDistance = Integer.MAX_VALUE;
		Pair closestPair = null;
		for (int i = 0; i < length; i++) {
			for (int j = i + 1; j < length; j++) {
				Pair pair = new Pair(points.get(i), points.get(j));
				float d = pair.distance(); 
				if (d < closestDistance) {
					closestDistance = d;
					closestPair = pair;
				}
			}
		}
		return closestPair;
	}
	
	public class Pair {
		run.Point p1;
		run.Point p2;
		
		public Pair(run.Point p1, run.Point p2) {
			this.p1 = p1;
			this.p2 = p2;
		}
		
		public float distance() {
			double diffX = p1.x - p2.x;
			double diffY = p1.y - p2.y;
			return (float) Math.sqrt(Math.abs(Math.pow(diffX, 2) + Math.pow(diffY, 2)));
		}
		
	}
	
}
