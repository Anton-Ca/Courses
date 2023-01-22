package Hanoi;

import java.util.ArrayList;
import java.util.Scanner; 

public class Peg {
		private ArrayList<Disk> disks;

		/** Tar reda på numret på den översta brickan, Integer.MAX_VALUE om pinnen är tom. */
		public int getTopDiskSize(){
			return (! disks.isEmpty())?
			disks.get(disks.size()-1).getSize():
		Integer.MAX_VALUE;
	}

	/** Lägger brickan d överst på pinnen. */
	public void putDisk(Disk d) {
		disks.add(d);
		/**if (d == null)
		 throw new IllegalArguementException(“The argument cannot be null”);
		return d.length();
	*/}

	/** Hämtar och tar bort den översta brickan. */
	public Disk getDisk(){
		Disk d = disks.remove(disks.size()-1);
		return d;
	}
}
