package lab4;

import java.util.*;

public class solution3 {
	public solution3(ArrayList<lab4.run2.Point> points) {
		long a = System.currentTimeMillis();
		// sortedPoints = mergeSort(points);
		points.sort(Comparator.comparingInt(p -> p.x));
		long b = System.currentTimeMillis();
		// System.out.println("TIME TO CRETE GRAPH: " + (b - a) + "\n");

		a = System.currentTimeMillis();
		System.out.println(solve(points));
		b = System.currentTimeMillis();
		// System.out.println("TIME TO EXECUTE ALGORITHM: " + (b - a) + "\n");
		System.out.println("SIZE = " + points.size() + " POINTS: " + points.toString());
	}

	public double solve(ArrayList<lab4.run2.Point> points) {
		ArrayList<lab4.run2.Point> sortedXPoints = new ArrayList<>();
		ArrayList<lab4.run2.Point> yPoints = new ArrayList<>();
		
		for (int i = 0; i < points.size(); i++) {
			sortedXPoints.add(points.get(i));
			yPoints.add(points.get(i));
		}
		
		sortedXPoints.sort(Comparator.comparingInt(p -> p.x));
		
		return findClosestPair(sortedXPoints, yPoints, sortedXPoints.size());
	}
	
	public double findClosestPair(ArrayList<lab4.run2.Point> sortedXPoints, ArrayList<lab4.run2.Point> yPoints, int nbrOfPoints) {
		
		// Brute force if less than or equal amount to 3 points (constant timeoperations) 
		if (nbrOfPoints <= 3) {
			return bruteForce(sortedXPoints);
		}
		
		int midIndex = nbrOfPoints/2;
		
		// Divide into left and right sub-arrays 
		ArrayList<lab4.run2.Point> leftSubY = new ArrayList<>();
		ArrayList<lab4.run2.Point> leftSubXSorted =new ArrayList<>() ;
		ArrayList<lab4.run2.Point> rightSubY =new ArrayList<>();
		ArrayList<lab4.run2.Point> rightSubXSorted =new ArrayList<>() ;
		
		for (int i = 0; i < nbrOfPoints; i++) {
			if(yPoints.get(i).x <= yPoints.get(midIndex).x) {
				leftSubY.add(yPoints.get(i));
				leftSubXSorted.add(sortedXPoints.get(i));
			} else {
				rightSubY.add(yPoints.get(i));
				rightSubXSorted.add(sortedXPoints.get(i));
			}
		}
		
		// Recursive search
		double dLeft = findClosestPair(leftSubXSorted, leftSubY, midIndex);
		double dRight = findClosestPair(rightSubXSorted, rightSubY, nbrOfPoints - midIndex);
		double dBoth = Math.min(dLeft, dRight);
		
		ArrayList<lab4.run2.Point> pointsWithinStrip = new ArrayList<lab4.run2.Point>();
		
		// Find smallest distance in strip with width 2*dBoth
		for (int i = 0; i < nbrOfPoints; i++) {
			if (Math.abs(yPoints.get(i).x - yPoints.get(midIndex).x) < dBoth) {
				pointsWithinStrip.add(yPoints.get(i));
			}
		}
		
		double minDistStrip = findMinDistanceInStrip(pointsWithinStrip, dBoth);
		
		return Math.min(dBoth, minDistStrip);
	}
		
	public double bruteForce(ArrayList<lab4.run2.Point> points) {
		double minDistance = Integer.MAX_VALUE;
		
		for (int i = 0; i < points.size(); i++) {
			for (int j = i + 1; j < points.size(); j++) {
				if (distance(points.get(i), points.get(i)) < minDistance) {
					minDistance = distance(points.get(i), points.get(i));
				}
			}
		}
		return minDistance;
	}
	
	public double findMinDistanceInStrip(ArrayList<lab4.run2.Point> points, double minD) {
		double minDistance = minD;
		
		for (int i = 0; i < points.size(); i++) {
			for (int j = i + 1; j < points.size() && (points.get(i).y - points.get(i).y) < minD; j++) {
				if (distance(points.get(i), points.get(i)) < minDistance) {
					minDistance = distance(points.get(i), points.get(i));
				}
			}
		}
		return minDistance;
	}
	
	public double distance(lab4.run2.Point p1, lab4.run2.Point p2) {
		double diffX = Math.abs(p1.x - p2.x);
		double diffY = Math.abs(p1.y - p2.y);
		return (double) Math.sqrt(diffX*diffX + diffY*diffY); 
	}
	
}