package testqueue;

import static org.junit.Assert.*;
import org.junit.Test;
import org.junit.After;
import org.junit.Before;
import java.util.Queue;
import java.util.Iterator;
import java.lang.IllegalArgumentException;

import queue_singlelinkedlist.FifoQueue2;

public class TestAppendFifoQueue {

	private FifoQueue2<Integer> myIntQueue;
	private FifoQueue2<Integer> myIntQueue2;
        private FifoQueue2<String> myStringQueue;

	@Before
        public void setUp() throws Exception {
                myIntQueue = new FifoQueue2<Integer>();
                myStringQueue = new FifoQueue2<String>();
        	myIntQueue2 = new FifoQueue2<Integer>();
        }   

        @After
        public void tearDown() throws Exception {
                myIntQueue = null;
                myStringQueue = null;
		myIntQueue = null;
	}
// Jag duplicerade några av testfallen och testade så att allt fungerar för båda köerna, så man vet att det fungerar för köer med olika objekt. Egentligen onödigt. 
 
	/** 
         * Test if newly created queues are empty.
         */
        @Test
        public final void testNewFifoQueue2() {
                assertTrue(myIntQueue.isEmpty());
                assertTrue(myIntQueue.size() == 0); 
		assertTrue(myStringQueue.isEmpty());
                assertTrue(myStringQueue.size() == 0); 
		
        }

 /** Test a single offer followed by a single peek. */
        @Test
        public final void testPeek() {
                myIntQueue.offer(1);
                myStringQueue.offer("1");
                int i = myIntQueue.peek();
		String str = myStringQueue.peek();
                assertEquals("peek on queue of size 1", 1, i);
                assertTrue(myIntQueue.size() == 1);
                assertTrue(myStringQueue.size() == 1);
        
        }
	
	/**
         * Test a single offer followed by a single poll.
         */
        @Test
        public final void testPoll() {
                myIntQueue.offer(1);
                myStringQueue.offer("1");
                int i = myIntQueue.poll();
                String str = myStringQueue.poll();
                assertEquals("poll on queue of size 1", 1, i);
                assertTrue("Wrong size after poll", myIntQueue.size() == 0);
                assertTrue("Wrong size after poll", myStringQueue.size() == 0);
        
        }

	/**
	* Test creating two non-empty queues 
	*/
	@Test
	public final void testNoEmpty() {
		myIntQueue.offer(1);
                myStringQueue.offer("2");
		assertTrue("Wrong size.", myIntQueue.size() != 0);
	} 

	/**
	* Test one offer followed by adding two queues together.
	*/
	@Test
	public final void testAppendDifferent() {
		myIntQueue.offer(1);
        	myIntQueue2.offer(2);
                myIntQueue.append(myIntQueue2);
		assertTrue("Wrong size after appending", myIntQueue.size() == 0);
		assertTrue("Second queue has wrong size after appending.", myIntQueue2.size() != 0);	

	}
	/**
	* Test ordering of offer followed by adding two identical queues together.
	*/
	@Test
	public final void testAppendSame() {
		int nbr = 3;
		for (int i = 0; i < 3; i++){
			myIntQueue.offer(i);
		}
		Iterator<Integer> itr = myIntQueue.iterator();
		
		assertTrue("Wrong result from hasNext()", itr.hasNext());
		for (int i = 1; i <= nbr; i++) {
                         assertEquals("Wrong result from itr.next", Integer.valueOf(i), itr.next());
                 }
		
		try {
                	myIntQueue.append(myIntQueue);
			fail("Should raise IllegalArgumentException");
		} catch (IllegalArgumentException e){
			// Successful test
		}

	}
}

