package lab4;


// Ändra alla Point[] till ArrayList<Point>

import java.util.ArrayList;

public class MergeSort {
	
	public MergeSort(lab4.run2.Point[] points){
		mergeSort(points);
	}
	
	public lab4.run2.Point[] mergeSort(lab4.run2.Point[] points) {
		lab4.run2.Point[] tmpArray = new ArrayList<>(points.size());
		return sort(points, tmpArray, 0, points.size()); // Add size()() -1 if nullPointer
	}
	
	private lab4.run2.Point[] sort(lab4.run2.Point[] points, lab4.run2.Point[] tmpArray, int first, int last ) {
		if (first < last) {
			int mid = (first + last) / 2;
			sort(points, tmpArray, first, mid);
			sort(points, tmpArray, mid + 1, last);
			return merge(points, tmpArray, first, mid + 1, last);
		}
		return null;
	}

	@SuppressWarnings({ "unchecked", "rawtypes" })
	private lab4.run2.Point[] merge(lab4.run2.Point[] points, lab4.run2.Point[] tmpArray, int leftPos, int rightPos, int rightEnd) {
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



}
