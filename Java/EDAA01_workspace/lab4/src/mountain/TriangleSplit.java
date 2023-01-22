/**
 * 
 */
package mountain;

import fractal.*;

/**
 * @author AntonCarlsson
 *
 */
public class TriangleSplit extends Fractal {
	Point p1;
	Point p2;
	Point p3;

	/**
	 * Creates an object that handles Mountain's fractal.
	 * 
	 * @param length the length of the triangle side
	 */
	public TriangleSplit(Point p1, Point p2, Point p3) {
		super();
		this.p1 = p1;
		this.p2 = p2;
		this.p3 = p3;
	}

	/**
	 * Returns the title.
	 * 
	 * @return the title
	 */
	@Override
	public String getTitle() {
		return "TriangleSplit fractal";
	}

	/**
	 * Draws the fractal.
	 * 
	 * @param turtle the turtle graphic object
	 */
	@Override
	public void draw(TurtleGraphics turtle) {
		fractalTriangle(turtle, order, p1, p2, p3);
	}

	/*
	 * Reursive method: Draws a recursive line of the triangle.
	 */
	private void fractalTriangle(TurtleGraphics turtle, int order, Point p1, Point p2, Point p3) {
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
			// Förskjut triangeln och kalla på ny fractal
			fractalTriangle(turtle, order - 1, p1,
					new Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2),
					new Point((p1.getX() + p3.getX()) / 2, (p1.getY() + p3.getY()) / 2));
			fractalTriangle(turtle, order - 1,
					new Point((p1.getX() + p3.getX()) / 2, (p1.getY() + p3.getY()) / 2),
					new Point((p2.getX() + p3.getX()) / 2, (p2.getY() + p3.getY()) / 2), p3);
			fractalTriangle(turtle, order - 1,
					new Point((p1.getX() + p3.getX()) / 2, (p1.getY() + p3.getY()) / 2),
					new Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2),
					new Point((p2.getX() + p3.getX()) / 2, (p2.getY() + p3.getY()) / 2));
			fractalTriangle(turtle, order - 1,
					new Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2), p2,
					new Point((p2.getX() + p3.getX()) / 2, (p2.getY() + p3.getY()) / 2));
		}
	}
}
