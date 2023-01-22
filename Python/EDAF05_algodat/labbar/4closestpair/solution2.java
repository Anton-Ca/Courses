import java.util.*;

public class solution2 {
	private run2.Point[] points;

	public solution2(run2.Point[] points) {
		this.points = points;

		long a = System.currentTimeMillis();
		// sortedPoints = mergeSort(points);
		Arrays.sort(points, Comparator.comparingInt(p -> p.x));
		long b = System.currentTimeMillis();
		// System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");

		a = System.currentTimeMillis();
		System.out.println(findClosestPair(points));
		b = System.currentTimeMillis();
		// System.out.println("TIME TO EXECUTE ALGORITHM: " + (b - a) + "\n");
		System.out.println("SIZE = " + points.length + " POINTS: " + points.toString());
	}

	// Sorting



	public float findClosestPair(run2.Point[] sortedPoints) {
		run2.Point[] sP = sortedPoints;
		int length = sP.length;

		if (length < 4)
			return bruteForce(length).distance();

		run2.Point[] left = new run2.Point[sP.length / 2];
		run2.Point[] right = new run2.Point[sP.length / 2];

		for (int i = 0; i < sP.length; i++) {
			if (i < sP.length / 2)
				left[i] = sP[i];

			if (i > sP.length / 2)
				right[i] = sP[i];
		}

		float distanceLeft = findClosestPair(left);
		float distanceRight = findClosestPair(right);
		float distanceBoth = Integer.MAX_VALUE;
		float distanceFinal = Integer.MAX_VALUE;

		if (distanceLeft > distanceRight)
			distanceBoth = distanceRight;
		else
			distanceBoth = distanceLeft;

		run2.Point[] sortedByY = new run2.Point[length]; // Osäker här
		float dY = Integer.MAX_VALUE;

		for (int i = 0; i < length; i++) {
			if (sP[length / 2 - 1].x - distanceBoth < sP[i].x && sP[i].x < sP[length / 2 - 1].x + distanceBoth)
				sortedByY[i] = sP[i];
		}

		Arrays.sort(sortedByY, Comparator.comparingInt(p -> p.y));
		
		if (sortedByY.length == 1) {
			distanceFinal = distanceBoth;
		} else if (sortedByY.length < 8) {
			dY = bruteForce(sortedByY.length).distance();
			if (distanceBoth > dY) {
				distanceFinal = dY;
			} else {
				distanceFinal = distanceBoth;
			}
		} else {
			for (int i = 0; i < sortedByY.length; i++) {
				for (int j = i + 1; j < sortedByY.length; j++) {
					dY = bruteForce(sortedByY[i].y).distance(); //Vad fan händer här
				}
				
				if (distanceBoth > dY) {
					distanceFinal = dY;
				} else {
					distanceFinal = distanceBoth;
				}
			}
		}
		
		return distanceFinal;
	}

	public Pair bruteForce(int length) {
		float closestDistance = Integer.MAX_VALUE;
		Pair closestPair = null;
		for (int i = 0; i < length; i++) {
			for (int j = i + 1; j < length; j++) {
				Pair pair = new Pair(points[i], points[j]);
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
		run2.Point p1;
		run2.Point p2;

		public Pair(run2.Point p1, run2.Point p2) {
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
