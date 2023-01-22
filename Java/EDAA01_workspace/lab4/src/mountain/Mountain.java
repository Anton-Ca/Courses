/**
 * 
 */
package mountain;

import fractal.*;
import java.lang.*;
import java.util.HashMap;
import java.util.Map;

/**
 * @author AntonCarlsson
 *
 */
public class Mountain extends Fractal {
	Point p1, p2, p3;
	double dev;
	Map<Side, Point> m;

	/**
	 * Creates an object that handles Mountain's fractal.
	 * 
	 * @param length the length of the triangle side
	 */
	public Mountain(Point p1, Point p2, Point p3, double dev) {
		super();
		this.p1 = p1;
		this.p2 = p2;
		this.p3 = p3;
		this.dev = dev;
		m = new HashMap<Side, Point>();
	}

	/**
	 * Returns the title.
	 * 
	 * @return the title
	 */
	@Override
	public String getTitle() {
		return "Mountain fractal";
	}

	/**
	 * 
	 * @param dev
	 * @return a random number t
	 */
	public static double randFunc(double dev) {
		double t = dev * Math.sqrt(-2 * Math.log(Math.random()));
		if (Math.random() < 0.5) {
			t = -t;
		}
		return t;
	}

	/**
	 * Draws the fractal.
	 * 
	 * @param turtle the turtle graphic object, with three different points and a
	 *               deviance
	 */
	@Override
	public void draw(TurtleGraphics turtle) {
		fractalTriangle(turtle, order, p1, p2, p3, dev);
	}

	/*
	 * Reursive method: Draws a recursive line of the triangle.
	 */
	private void fractalTriangle(TurtleGraphics turtle, int order, Point p1, Point p2, Point p3, double dev) {
		if (order == 0) {
			// Hitta punkterna
			// Rita streck till punkterna.
			turtle.penUp();
			turtle.moveTo(p1.getX(), p1.getY());
			turtle.penDown();
			turtle.forwardTo(p2.getX(), p2.getY());
			turtle.forwardTo(p3.getX(), p3.getY());
			turtle.forwardTo(p1.getX(), p1.getY());

		} else {
			// Smidigare än att hantera punkterna var för sig
			// Måste ha med en sista p1 för att få mittpunkten mellan p1 & p3 i loopen
			// längre ner
			Point[] points = { p1, p2, p3, p1 };
			Point[] mid = new Point[3];

			// Insåg att man hade behövt upprepa mycket if-satser utan for loop
			for (int i = 0; i < mid.length; i++) {
				mid[i] = new Point(0, 0);
				Side s = new Side(points[i], points[i + 1]);
				if (m.containsKey(s)) {
					mid[i] = m.get(s);
				 
				} else {
					mid[i] = new Point((int) (points[i].getX() + points[i + 1].getX()) / 2,
							(int) (points[i].getY() + points[i + 1].getY()) / 2 + (int) randFunc(dev));
					m.put(new Side(points[i], points[i + 1]), mid[i]);
				}
			}

//			p13 = new Point((p1.getX() + p3.getX()) / 2, (p1.getY() + p3.getY()) / 2 + (int) randFunc(dev));
//			p23 = new Point((p2.getX() + p3.getX()) / 2, (p2.getY() + p3.getY()) / 2 + (int) randFunc(dev));
			// Förskjut triangeln och kalla på ny fractal, har även bytt ordning från
			// föregående uppgift till så som det ska vara ifall man läser uppgiften.
			fractalTriangle(turtle, order - 1, p1, mid[0], mid[2], dev / 2);
			fractalTriangle(turtle, order - 1, mid[0], p2, mid[1], dev / 2);
			fractalTriangle(turtle, order - 1, mid[2], mid[1], p3, dev / 2);
			fractalTriangle(turtle, order - 1, mid[0], mid[1], mid[2], dev / 2);

		}
	}

	class Side {
		public Point a, b;

		public Side(Point a, Point b) {
			this.a = a;
			this.b = b;

		}

		public Point getPointA() {
			return a;
		}

		public Point getPointB() {
			return b;
		}

		@Override
		public boolean equals(Object obj) {
			if (obj instanceof Side) {
				Side s = (Side) obj;
				return (a.equals(s.a) && b.equals(s.b)) || (a.equals(s.b) && b.equals(s.a));
//				return this.equals(s) || this.equals(new Side(s.getPointB(), s.getPointA()));
			}
			return false;
		}

		@Override
		public int hashCode() {
			return a.hashCode() + b.hashCode();
		}
	}
}
