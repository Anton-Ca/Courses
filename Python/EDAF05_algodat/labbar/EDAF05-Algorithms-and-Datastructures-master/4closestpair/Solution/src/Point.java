import java.util.Map;

public class Point{

    int x;
    int y;
    public Point (int x, int y)
    {
        this.x = x;
        this.y = y;

    }
    public double distanceTo(Point other)
    {
        return Math.sqrt(Math.pow(other.x-x,2)+ Math.pow(other.y-y,2));
    }

    int getX()
    {
        return x;
    }

    int getY()
    {
        return y;
    }
    @Override
    public String toString()
    {
        return "(" + x +","+y+")";
    }

    @Override
    public boolean equals(Object other)
    {
        if( !(other instanceof  Point))
            return false;
        return (this.x == ((Point) other).x) && (this.y == ((Point) other).y);
    }
}
