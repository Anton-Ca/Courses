package Hanoi;
import Hanoi;

import java.util.ArrayList;
import java.util.Scanner;
 
// import java.lang.IllegalArgumentException;

public class TowersOfHanoi {
	public static void main(String[] args){
		System.out.println("Antal brickor: ");
		Scanner scan = new Scanner(System.in);
		int nbrDisks = scan.nextInt();
		HanoiBoard board = new HanoiBoard(nbrDisks);
		HanoiStrategy strategy = new HanoiStrategy(board);
		strategy.moveDisks();
		// if (board == null)
  //               	throw new IllegalArguementException("The argument cannot be null");
 	// 		return board.length();
	}
}
