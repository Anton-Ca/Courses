import java.util.*;
import java.text.DecimalFormat;

public class solution3 {
	private run2.Point[] points;

	public solution3(run2.Point[] points) {
		this.points = points;

		long a = System.currentTimeMillis();
		// sortedPoints = mergeSort(points);
		Arrays.sort(points, Comparator.comparingInt(p -> p.x));
		long b = System.currentTimeMillis();
		// System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");

		DecimalFormat df = new DecimalFormat("#.000000");

		a = System.currentTimeMillis();
		System.out.println(df.format(solve(points)));
		b = System.currentTimeMillis();
		// System.out.println("TIME TO EXECUTE ALGORITHM: " + (b - a) + "\n");
		//System.out.println("SIZE = " + points.length + " POINTS: " + points.toString());
	}

	public double solve(run2.Point[] points) {
		run2.Point[] sortedXPoints = new run2.Point[points.length];
		run2.Point[] yPoints = new run2.Point[points.length];
		run2.Point midPoint = null;
		
		for (int i = 0; i < points.length; i++) {
			sortedXPoints[i] = points[i];
			yPoints[i] = points[i];
			if (i == points.length/2)
				midPoint = points[i];
		}
		
		Arrays.sort(sortedXPoints, Comparator.comparingInt(p -> p.x));
		
		return findClosestPair(sortedXPoints, yPoints, sortedXPoints.length, midPoint);
	}
	
	public double findClosestPair(run2.Point[] sortedXPoints, run2.Point[] yPoints, int nbrOfPoints, run2.Point midPoint) {
		
		// Brute force if less than or equal amount to 3 points (constant timeoperations) 
		if (nbrOfPoints <= 3) {
			return bruteForce(sortedXPoints);
		}
		
		int midIndex = nbrOfPoints/2;
		run2.Point newMidPoint = null;
		
		// Divide into left and right sub-arrays 
		run2.Point[] leftSubY = new run2.Point[nbrOfPoints - nbrOfPoints/2];
		run2.Point[] leftSubXSorted = new run2.Point[nbrOfPoints - nbrOfPoints/2];
		run2.Point[] rightSubY = new run2.Point[nbrOfPoints/2];
		run2.Point[] rightSubXSorted = new run2.Point[nbrOfPoints/2];
		
		System.out.println(nbrOfPoints);
		for (int i = 0; i < nbrOfPoints; i++) { 
			//System.out.println("i = " + i + " | NUMBER OF POINTS = " + nbrOfPoints);

			// yPoints verkar bli null efter midIndex operationer
			if(yPoints[i].x <= midPoint.x) {
				System.out.println("L");
				//System.out.println(yPoints[i].toString() + " < " + midPoint.toString() + "\n");
				leftSubY[i] = yPoints[i];
				leftSubXSorted[i] = sortedXPoints[i];
			} else {
				//if (rightSubY[i] == null)
				//	continue;

				System.out.println("R");
				//System.out.println(rightSubY[i].toString() + " > " + midPoint.toString() + "\n");
				rightSubY[i] = yPoints[i];
				rightSubXSorted[i] = sortedXPoints[i];
			}
			if (i == midIndex)
				newMidPoint = points[i];

			System.out.println("i = " + i + " | NUMBER OF POINTS = " + nbrOfPoints);
		}
		
		// Recursive search
		double dLeft = findClosestPair(leftSubXSorted, leftSubY, midIndex, newMidPoint);
		double dRight = findClosestPair(rightSubXSorted, rightSubY, nbrOfPoints - midIndex, newMidPoint);
		double dBoth = Math.min(dLeft, dRight);
		int stripPoints = 0;
	
		// Find amount of points on the strip with 2*dBoth width	
		for (int i = 0; i < nbrOfPoints; i++) {
			if (Math.abs(yPoints[i].x - midPoint.x) < dBoth) 
				stripPoints++;
		}

		run2.Point[] pointsWithinStrip = new run2.Point[stripPoints];
		
		// Find smallest distance between points on strip
		for (int i = 0; i < nbrOfPoints; i++) {
			if (Math.abs(yPoints[i].x - midPoint.x) < dBoth) 
				pointsWithinStrip[i] = yPoints[i];	
		}
		
		double minDistStrip = findMinDistanceInStrip(pointsWithinStrip, dBoth);
		
		return Math.min(dBoth, minDistStrip);
	}
		
	public double bruteForce(run2.Point[] sortedPoints) {
		double minDistance = Integer.MAX_VALUE;
		
		for (int i = 0; i < sortedPoints.length; i++) {
			for (int j = i + 1; j < sortedPoints.length; j++) {
				if (distance(sortedPoints[i], sortedPoints[j]) < minDistance) {
					minDistance = distance(sortedPoints[i], sortedPoints[j]);
					
				}
			}
		}
		return minDistance;
	}
	
	public double findMinDistanceInStrip(run2.Point[] points, double minD) {
		double minDistance = minD;
		
		for (int i = 0; i < points.length; i++) {
			for (int j = i + 1; j < points.length; j++) {
				if((points[j].y - points[i].y) < minD)	
					if (distance(points[i], points[j]) < minD) {
						minDistance = distance(points[i], points[j]);
							
				}
			}
		}
		return minDistance;
	}
	
	public double distance(run2.Point p1, run2.Point p2) {
		double diffX = Math.abs(p1.x - p2.x);
		double diffY = Math.abs(p1.y - p2.y);
		return (double) Math.sqrt(diffX*diffX + diffY*diffY); 
	}
	
}
