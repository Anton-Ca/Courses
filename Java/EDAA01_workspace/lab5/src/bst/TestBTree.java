/**
 * 
 */
package bst;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import java.util.Comparator;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * @author AntonCarlsson
 *
 */
class TestBTree {
	Comparator<String> comps;
	Comparator<Integer> compi;
	BinarySearchTree<String> str;
	BinarySearchTree<Integer> nbr;

	/**
	 * @throws java.lang.Exception 
	 * BeforeEach istället för Before då vi är i J-Unit
	 * 5 istället för 4 som tidigare
	 */
	@BeforeEach
	public void setUp() throws Exception {
		comps = (s1, s2) -> ((Comparable<String>) s1).compareTo(s2);
		compi = (i1, i2) -> ((Comparable<Integer>) i1).compareTo(i2);
		str = new BinarySearchTree<String>();
		nbr = new BinarySearchTree<Integer>(compi);
	}

	/**
	 * @throws java.lang.Exception
	 */
	@AfterEach
	public void tearDown() throws Exception {
		comps = null;
		compi = null;
		str = null;
		nbr = null;
	}

	/**
	 * Kontrollerar size för tomma BinarySearchTrees.
	 */
	@Test
	public void testEmpty() {
		str.clear();
		nbr.clear();
		assertTrue("Fel värde för ett tomt träd", str.size() == 0);
		assertTrue("Fel värde för ett tomt träd", nbr.size() == 0);
	}

	/**
	 * Kontrollerar height för ett tomt träd.
	 */
	@Test
	public void testHeightEmpty() {
		str.clear();
		nbr.clear();
		assertEquals("Fel height", str.height(), 0);
		assertEquals("Fel värde för trädet", nbr.height(), 0);
	}

	/**
	 * Kontrollerar height för et icke-tomt träd.
	 */
	@Test
	public void testHeight() {
		String[] s = { "boi", "lit", "XBox", "Playstation", "Cool" };
		for (String astr : s)
			str.add(astr);
		Integer[] n = { 69, 420, 360, 37, 0 };
		for (int i : n)
			nbr.add(i);
		assertEquals("Fel height", str.height(), 4);
		assertEquals("Fel värde för trädet", nbr.height(), 3);
	}

	/**
	 * Kontrollerar size för add BinarySearchTrees och att size uppdateras korrekt.
	 */
	@Test
	public void testAdd() {
		str.add("boi");
		nbr.add(69);
		assertTrue("Fel värde för trädet", str.size() == 1);
		assertTrue("Fel värde för trädet", nbr.size() == 1);
		str.add("lit");
		nbr.add(420);
		assertTrue("Fel värde för trädet", str.size() == 2);
		assertTrue("Fel värde för trädet", nbr.size() == 2);
		assertEquals("Fel vid insättning av element.", str.root.element, "boi");
		assertEquals("Fel vid insättning av int element.",(int) nbr.root.element,(int) 69);
	}

	/**
	 * Kontrollerar att dubletter ej är tillåtet BinarySearchTrees.
	 */
	@Test
	public void testAddDuplicate() {
		str.add("boi");
		nbr.add(69);
		assertFalse("Fel värde för trädet", str.size() != 1);
		assertFalse("Fel värde för trädet", nbr.size() != 1);
		str.add("boi");
		nbr.add(69);
		assertFalse("Fel värde för trädet", str.size() != 1);
		assertFalse("Fel värde för trädet", nbr.size() != 1);
		assertEquals("Fel vid insättning av element.", str.add("boi"), false);
		assertEquals("Fel vid insättning av element.", nbr.add(69), false);
	}

}
