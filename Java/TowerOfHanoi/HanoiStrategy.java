package Hanoi;

import java.util.ArrayList;
import java.util.Scanner; 
public class HanoiStrategy {
	private HanoiBoard board;

	/** Skapar en strategi för att flytta brickor på spelplanen board. */
	public HanoiStrategy(HanoiBoard board){
		this.board = board; 
	}

	/** Flyttar brickorna på pinne 1 till en annan pinne. */
	public void moveDisks() {
		int moveNbr = 1;
		while(! board.isFinished()){
			moveOneDisk(moveNbr);
			moveNbr++;
		}
	}

	/** Flyttar en brickaenligt reglerna i drag nummer moveNbr, skriver ut flyttningen. */ 
	private void moveOneDisk(int moveNbr) {
		int Peg1 = board.getPegWithDiskOne();
		int from; // Pinne att flitta en bricka från.
		int to; // Pinne att flytta en bricka till.
		if (moveNbr % 2 != 0) {
			// Udda drag.
			from = Peg1;
			to = (from + 1) % 3;
		} else {
			// Jämt drag.
			from = (Peg1 + 1) % 3;
			to = (from +1) % 3;
			// Se till att den minsta brickan flyttas. 
			if (board.getTopDiskSize(from) > board.getTopDiskSize(to)) {
				int temp = from;
				from = to;
				to = temp;
			}
		}
		System.out.println("Flytta bricka " + board.getTopDiskSize(from) + " från pinne " + (from +1) + " till pinne " + (to +1));
		board.moveDisk(from, to);
	}
}
