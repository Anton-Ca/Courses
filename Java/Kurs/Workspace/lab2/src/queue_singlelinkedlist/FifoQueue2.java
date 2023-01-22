package queue_singlelinkedlist;
import java.util.*;

import java.lang.IllegalArgumentException;

public class FifoQueue2<E> extends AbstractQueue<E> implements Queue<E> {
	private QueueNode<E> last;
	private int size;

	public FifoQueue2() {
		super();
		last = null;
		size = 0;
	}

	/**	
	 * Inserts the specified element into this queue, if possible
	 * post:	The specified element is added to the rear of this queue
	 * @param	e the element to insert
	 * @return	true if it was possible to add the element 
	 * 			to this queue, else false
	 */
	public boolean offer(E e) {
		size++;
		if(last == null){
			QueueNode<E> node = new QueueNode<E>(e); 
			last = node;
			last.next = node;
		} else {
			QueueNode<E> node = new QueueNode<E>(e);
			node.next = last.next; //node.next pekar på första elementet
			last.next = node; // last.next pekar på node som nu alltså är sist 
			last = node; // last uppdateras till node
		}
		return true;
	}
	
	/**	
	 * Returns the number of elements in this queue
	 * @return the number of elements in this queue
	 */
	public int size() {		
		return size;
	}
	
	/**	
	 * Retrieves, but does not remove, the head of this queue, 
	 * returning null if this queue is empty
	 * @return 	the head element of this queue, or null 
	 * 			if this queue is empty
	 */
	public E peek() {
		if(last == null){
			return null;
		} else {
			return last.next.element;
		}
	}

	/**	
	 * Retrieves and removes the head of this queue, 
	 * or null if this queue is empty.
	 * post:	the head of the queue is removed if it was not empty
	 * @return 	the head of this queue, or null if the queue is empty 
	 */
	public E poll() {
		if(last == null){
			return null;
		} else if (size == 1) {
			QueueNode<E> temp = last;
			last = null;
			last.next = null;
			size--;
			return temp.element;
		} else {
			QueueNode<E> temp = last.next;
			last.next = last.next.next;
			size--;
			return temp.element;
		}
	}
	
	public class QueueIterator implements Iterator<E>{
		private QueueNode<E> pos;
		private boolean start = true;
		/** Skapar en itterator på platsen last. Vill undvika att kolla om listan är tom.
		*/
		private QueueIterator(){
			if(last != null){
				pos = last.next;
			} 
		}
	
		public boolean hasNext(){
			if(pos != last && pos != last.next){
				return true;
			} else {
				return false;
			}
		}

		public E next(){
			if(hasNext()){
				QueueNode<E> temp = pos;
				if(pos == last && start != true ){
					pos = null;
				}
				pos = pos.next;
				start = false;
				return temp.element; 
			} else {
				throw new NoSuchElementException("Något gick snett!");
			}
		} 

	}

	/**	
	 * Returns an iterator over the elements in this queue
	 * @return an iterator over the elements in this queue
	 */	
	public Iterator<E> iterator() {
		return new QueueIterator();
	}
	
	/**
	* Appends the specified queue to this queue
	* post: all elements from the specified queue are appended
	* to this queue. The specified queue (q) is empty after the call.
	* @param q the queue to append
	* @throws IllegalArgumentException if this queue and q are identical
	*/
	public void append(FifoQueue2<E> q) throws IllegalArgumentException {
		// This refererar till vårt objekt, så om man bara skriver this så refererar det till klassen. 
		if(this != q) {
			if(q.size() != 0){
				if (size == 0) {
					last = q.last;
					size = q.size();
					// Som det ser ut nu behöver vi även uppdatera kön queue, men det borde finnas en bättre lösning som gör att man helt kan undvika queue. 
				} else {
					size = this.size + q.size();
					q.last.next = this.last.next;	
					this.last.next = q.last.next;
					this.last = q.last; 
				}
			
			} else {
				throw new IllegalArgumentException("IllegalArgumentException! Identical queues not allowed."); 		
			}
		}
}	

	private static class QueueNode<E> {
		E element;
		QueueNode<E> next;

		private QueueNode(E x) {
			element = x;
			next = null;
		}
	}

}
