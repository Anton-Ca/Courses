package Hanoi;

import java.util.ArrayList;
import java.util.Scanner; 

public class Disk{
		private int size =2;

		/** Skapar en bricka med storleken size. */
		public Disk(int size){
			this.size = size;
		}

		/** Tar reda på brickans storlek. */
		public int getSize() {
		System.out.println(size);	
		return size;
		}

	}



// 	public class Peg {
// 		private ArrayList<Disk> disks;

// 		/** Tar reda på numret på den översta brickan, Integer.MAX_VALUE om pinnen är tom. */
// 		public int getTopDiskSize(){
// 			return (! disks.isEmpty())?
// 			disks.get(disks.size()-1).getSize():
// 		Integer.MAX_VALUE;
// 	}

// 	/** Lägger brickan d överst på pinnen. */
// 	public void putDisk(Disk d) {
// 		disks.add(d);
// 	}

// 	/** Hämtar och tar bort den översta brickan. */
// 	public Disk getDisk(){
// 		Disk d = disks.remove(disks.size()-1);
// 		return d;
// 	}
// }


// public class HanoiBoard{
// 	private Peg[] pegs;

// 	/** Skapar en spelplan med tre tomma pinnar, lägger nbrDisks på den första pinnen. */
// 	public HanoiBoard(int nbrDisks){
// 		pegs = new Peg[3];
// 		for (int i = 0; i < pegs.length; i++) {
// 			pegs[i] = new Peg();
// 		}
// 		for (int i = nbrDisks; i >= 1; i--) {
// 			pegs[0].putDisk(new Disk(i));
// 		}
// 	}

// 	/** Tar reda på numret på pinnen som innehåller bricka 1. */
// 	public int getPegWithDiskOne(){
// 		int Peg1 = 0;
// 		while (getTopDiskSize(Peg1) != 1) {
// 			Peg1++;
// 		}
// 		return Peg1;
// 	}

// 	/** Undersöker om spelet är slut. */
// 	public boolean isFinished() {
// 		return isEmpty(0) && 
// 			(isEmpty(1) || isEmpty(2));
// 	}

// 	/** Tar reda på storleken av den översta brickan på pinne nummer peg, Integer.MAX_VALUE om pinnen är tom. */
// 	public int getTopDiskSize(int peg) {
// 		return pegs[peg].getTopDiskSize();
// 	}

// 	/** Flyttar den översta brickan från pinne nummer from till pinne nummer to. */
// 	public void moveDisk(int from, int to){
// 		Disk d = pegs[from].getDisk();
// 		pegs[to].putDisk(d);
// 	}

// 	/** Undersöker om pinnen med nummer peg är tom. */
// 	private boolean isEmpty(int peg) {
// 		return pegs[peg].getTopDiskSize() == 
// 			Integer.MAX_VALUE;
// 	}
// }


// public class HanoiStrategy {
// 	private HanoiBoard board;

// 	/** Skapar en strategi för att flytta brickor på spelplanen board. */
// 	public HanoiStrategy(HanoiBoard board){
// 		this.board = board; 
// 	}

// 	/** Flyttar brickorna på pinne 1 till en annan pinne. */
// 	public void moveDisks() {
// 		int moveNbr = 1;
// 		while(! board.isFinished()){
// 			moveOneDisk(moveNbr);
// 			moveNbr++;
// 		}
// 	}

// 	/** Flyttar en brickaenligt reglerna i drag nummer moveNbr, skriver ut flyttningen. */ 
// 	private void moveOneDisk(int moveNbr) {
// 		int Peg1 = board.getPegWithDiskOne();
// 		int from; // Pinne att flitta en bricka från.
// 		int to; // Pinne att flytta en bricka till.
// 		if (moveNbr % 2 != 0) {
// 			// Udda drag.
// 			from = Peg1;
// 			to = (from + 1) % 3;
// 		} else {
// 			// Jämt drag.
// 			from = (Peg1 + 1) % 3;
// 			to = (from +1) % 3;
// 			// Se till att den minsta brickan flyttas. 
// 			if (board.getTopDiskSize(from) > board.getTopDiskSize(to)) {
// 				int temp = from;
// 				from = to;
// 				to = temp;
// 			}
// 		}
// 		System.out.println("Flytta bricka " + board.getTopDiskSize(from) + " från pinne " + (from +1) + " till pinne " + (to +1));
// 		board.moveDisk(from, to);
// 	}
// }


// public class TowersOfHanoi {
// 	public static void main(String[] args){
// 		System.out.println("Antal brickor: ");
// 		Scanner scan = new Scanner(System.in);
// 		int nbrDisks = scan.nextInt();
// 		HanoiBoard board = new HanoiBoard(nbrDisks);
// 		HanoiStrategy strategy = new HanoiStrategy(board);
// 		strategy.moveDisks();
// 	}
// }
