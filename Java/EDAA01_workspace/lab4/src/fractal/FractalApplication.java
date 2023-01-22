package fractal;

import koch.Koch;
import mountain.TriangleSplit;
import mountain.Mountain;
import mountain.Point;

public class FractalApplication {
	public static void main(String[] args) {
		Point p1 = new Point(50, 450);
		Point p2 = new Point(300, 50);
		Point p3 = new Point(550, 550);
		int dev = 30;
		Fractal[] fractals = new Fractal[3];
		fractals[2] = new Koch(300);
		fractals[1] = new TriangleSplit(p1, p2, p3);
		fractals[0] = new Mountain(p1, p2, p3, dev);
	    new FractalView(fractals, "Fraktaler", 600, 600);
	}

}
