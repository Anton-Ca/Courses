package lpt;

import java.util.ArrayList;
import java.util.List;

public class Scheduler {
	private Machine[] machines;

// Fixa felet genom att byta ut Machine[] machines = machineArray; mot this ... se nedan. Felet beror på att machines ovan aldrig tilldelas ett värde och på så vis pekar på ett nullobjekt. 	
	/** Skapar en schemaläggare för maskinerna 
		i vektorn machines. */
	public Scheduler(Machine[] machineArray) {
		 this.machines = machineArray;
	}
	
// Returnerar den maskin som har minst att göra. 
	// (int i = 0, i < machines.length, i++) 
	public  Machine machineWithLeastToDo() {
		int min = Integer.MAX_VALUE;
		int minPuss = -1;
		for (int i = 0; i < machines.length; i++) {
			int totalTime = machines[i].getScheduledTime();
			if (totalTime < min) {
				min = totalTime;
				minPuss = i;
			}
		}
		return machines[minPuss];
	} 


	/* Returnerar den maskin som har minst att göra. */
	// (int i = 0, i < machines.length, i++) 

	/*public  Machine machineWithLeastToDo() {
		int min = Integer.MAX_VALUE;
		int minPuss = 0;
		for (Machine i : machines) {
			int totalTime = machines[i].getScheduledTime();
			if (totalTime < min) {
				min = totalTime;
			}
		
				minPuss++;
		}
	//tempJobList.sort(new DescTimeComp()); 
	/** Fördelar jobben i listan jobs på maskinerna. */
	public void makeSchedule(List<Job> jobs) {
		List<Job> tempJobList = new ArrayList<>(jobs);
		tempJobList.sort(new DescTimeComp());  //Hur sorterar sort natural ordering, Comparable - använder compareTo
		for (Job j : tempJobList) {
			Machine m = machineWithLeastToDo();	
			m.assignJob(j);
		}	
	}
	
	/** Tar bort alla jobb från maskinerna. */
	public void clearSchedule() {
		for(int i = 0; i < machines.length; i++) {
			machines[i].clearJobs();
		}	
	}

	/** Skriver ut maskinernas scheman. 
	public void printSchedule() {
		for (int i = 0; i <= machines.length; i++) {
			System.out.println(machines[i]);
		}
	}*/
	/** Skriver ut maskinernas scheman. */
	// Fixa felet OutOfBoundsException genom att ta bort "=" i for loopen.
	public void printSchedule() {
		for (int i = 0; i < machines.length; i++) {
			System.out.println(machines[i]);
		}
	}

}
