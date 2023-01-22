package Hanoi;

import java.util.ArrayList;
import java.util.Scanner; 
public class HanoiBoard{
	private Peg[] pegs;

	/** Skapar en spelplan med tre tomma pinnar, lägger nbrDisks på den första pinnen. */
	public HanoiBoard(int nbrDisks){
		pegs = new Peg[3];
		for (int i = 0; i < pegs.length; i++) {
			pegs[i] = new Peg();
		}
		for (int i = nbrDisks; i >= 1; i--) {
			pegs[0].putDisk(new Disk(i));
		}
	}

	/** Tar reda på numret på pinnen som innehåller bricka 1. */
	public int getPegWithDiskOne(){
		int Peg1 = 0;
		while (getTopDiskSize(Peg1) != 1) {
			Peg1++;
		}
		return Peg1;
	}

	/** Undersöker om spelet är slut. */
	public boolean isFinished() {
		return isEmpty(0) && 
			(isEmpty(1) || isEmpty(2));
	}

	/** Tar reda på storleken av den översta brickan på pinne nummer peg, Integer.MAX_VALUE om pinnen är tom. */
	public int getTopDiskSize(int peg) {
		return pegs[peg].getTopDiskSize();
	}

	/** Flyttar den översta brickan från pinne nummer from till pinne nummer to. */
	public void moveDisk(int from, int to){
		Disk d = pegs[from].getDisk();
		pegs[to].putDisk(d);
	}

	/** Undersöker om pinnen med nummer peg är tom. */
	private boolean isEmpty(int peg) {
		return pegs[peg].getTopDiskSize() == 
			Integer.MAX_VALUE;
	}
}
