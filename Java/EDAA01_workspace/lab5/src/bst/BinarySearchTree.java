package bst;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Random;

public class BinarySearchTree<E> {
	BinaryNode<E> root; // Används också i BSTVisaulizer
	int size; // Används också i BSTVisaulizer
	private Comparator<E> comp;

	public static void main(String[] args) throws IOException, InterruptedException {
		BSTVisualizer bstv = new BSTVisualizer("Tree", 900, 600);
		BinarySearchTree<Integer> bsti = new BinarySearchTree<Integer>();
		BinarySearchTree<String> bsts = new BinarySearchTree<String>();
		int[] a = { 1, 2, 33, 3, 4, 27, 5, 6, 69, 7, 8, 9, 0 };
		String[] b = { "d", "a", "f", "c", "e", "b", "g", "ö", "0" };

		Random rand = new Random();
		int[] vektor = new int[rand.nextInt(30)];
		int c = rand.nextInt(100) - 20; // Om jag addar c här får jag samma random tal varje gång

		for (int i : vektor)
			bsti.add(rand.nextInt(100) - 20);

//		for (int i : a) 
//			bsti.add(i);

		for (String str : b)
			bsts.add(str);

		bsti.printTree();
		bstv.drawTree(bsti);
		bsts.printTree();
		bstv.drawTree2(bsts);
		System.out.println("Press enter in console to rebuild tree");
		System.in.read();
		bsti.rebuild();
		bstv.drawTree(bsti);
		bstv.drawTree2(bsts);
	}

	/**
	 * Constructs an empty binary search tree.
	 */
	@SuppressWarnings("unchecked")
	public BinarySearchTree() {
		root = null;
		size = 0;
// 			Vad som händer i Lambdauttrycket nedan
//			comp = new Comparator<E>() {
//			@Override
//			public int compare(E o1, E o2) {
//				return ((Comparable<E>) o1).compareTo(o2);
//			}
//		};
		comp = (o1, o2) -> ((Comparable<E>) o1).compareTo(o2);
	}

	/**
	 * Constructs an empty binary search tree, sorted according to the specified
	 * comparator.
	 */
	public BinarySearchTree(Comparator<E> comp) {
		root = null;
		size = 0;
		this.comp = comp;
	}

	/**
	 * Inserts the specified element in the tree if no duplicate exists.
	 * 
	 * @param x element to be inserted
	 * @return true if the the element was inserted
	 */
	public boolean add(E x) {
		BinaryNode<E> boi = new BinaryNode<E>(x);
		if (root == null) {
			size++;
			root = boi;
			return true;
		} else
			return add(x, root);
	}

	// Överlagring
	private boolean add(E x, BinaryNode<E> b) {
		if (comp.compare(x, b.element) < 0) {
			if (b.left == null) {
				b.left = new BinaryNode<E>(x);
				size++;
			} else
				return add(x, b.left);
		}
		if (comp.compare(x, b.element) > 0) {
			if (b.right == null) {
				b.right = new BinaryNode<E>(x);
				size++;
			} else
				return add(x, b.right);
		}
		return false;
	}

	/**
	 * Computes the height of tree.
	 * 
	 * @return the height of the tree
	 */
	public int height() {
		if (root == null) {
			return 0;
		}
		return height(root);
	}

	// Överlagring
	private int height(BinaryNode<E> b) {
		if (b.left == null && b.right == null) {
			return 1;
		} else if (b.left == null) {
			return 1 + height(b.right);
		} else if (b.right == null) {
			return 1 + height(b.left);
		} else {
			return 1 + Math.max(height(b.right), height(b.left));
		}
	}

	/**
	 * Returns the number of elements in this tree.
	 * 
	 * @return the number of elements in this tree
	 */
	public int size() {
		return size;
	}

	/**
	 * Removes all of the elements from this list.
	 */
	public void clear() {
		root = null;
		size = 0;
	}

	/**
	 * Print tree contents in inorder.
	 */
	public void printTree() {
		printTree(root);
	}

	// Överlagring
	private void printTree(BinaryNode<E> b) {
		if (b != null) {
			printTree(b.left);
			System.out.println(b.element);
			printTree(b.right);
		}
	}

	/**
	 * Builds a complete tree from the elements in the tree.
	 */
	public void rebuild() {
		ArrayList<E> sorted = new ArrayList<E>();
		toArray(root, sorted);
		BinaryNode<E> newroot = buildTree(sorted, 0, sorted.size() - 1);
		root = newroot;
	}

	/*
	 * Adds all elements from the tree rooted at n in inorder to the list sorted in
	 * ascending order.
	 */
	private void toArray(BinaryNode<E> b, ArrayList<E> sorted) {
		if (b != null) {
			toArray(b.left, sorted);
			sorted.add(b.element);
			toArray(b.right, sorted);
		}
	}

	/*
	 * Builds a complete tree from the elements from position first to last in the
	 * list sorted. Elements in the list a are assumed to be in ascending order.
	 * Returns the root of tree.
	 */
	private BinaryNode<E> buildTree(ArrayList<E> sorted, int first, int last) {
		BinaryNode<E> midNode = null;
		int mid = first + (last - first) / 2;

		if (first <= last) {
			midNode = new BinaryNode<E>(sorted.get(mid));
			midNode.left = buildTree(sorted, first, mid - 1);
			midNode.right = buildTree(sorted, mid + 1, last);
		}
		return midNode;
	}

	static class BinaryNode<E> {
		E element;
		BinaryNode<E> left;
		BinaryNode<E> right;

		private BinaryNode(E element) {
			this.element = element;
		}
	}

}
