import java.util.ArrayList;
import java.util.Scanner;
import se.lth.cs.ptdc.window.SimpleWindow;

public class test{

	public static void main(String[] args){


		// Print stuff
		// System.out.println("Hello World");


		// If, elseif, else
		// int i = i;

		// if (i==5){
		// 	System.out.println("i is equal to " + i);
		// } else if(i>=5) {
		// 	System.out.println("i is greater than " + 5);			
		// } else if (i<=5){
		// 	System.out.println("i is less than " + 5);
		// } else {
		// 	System.out.println("i is not a number");
		// }
		// System.out.println(i);

		// Oändlig for loop 
		// ctr + c för att avbryta exekveringen 
		// for(int i = 5; i >= 0; i-- ){
		// 	System.out.println(i);
		// 	i++;
		// }

		// Skriver ut bokstaven efter a
		char c = 'a';
		c++;
		System.out.println(c);

		// Ritar fönster med kvadrat
		SimpleWindow w = new SimpleWindow(400, 400, "Square Test");
		Square sq = new square(10,20,50);
		sq.draw(w);
		sq.move(20,10);
		sq.draw(w);
	}

}

