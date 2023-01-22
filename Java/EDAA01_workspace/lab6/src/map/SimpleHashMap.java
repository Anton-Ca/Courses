package map;

import java.util.LinkedList;
import java.util.Random;

public class SimpleHashMap<K, V> implements Map<K, V> {
	private int capacity;
	private double load;
	private LinkedList<Entry<K, V>> list;
	private Entry<K, V>[] table;
	private int size;
	
	public static void main(String[] args) {
		SimpleHashMap<Integer, Integer> m = new SimpleHashMap<Integer, Integer>();
		Random rand = new Random();
		for (int i = 0; i < 1000; i++) {
			int n = rand.nextInt(1000);
			if (n % 2 == 0)
				m.put(n, n);
		}
		System.out.println(m.show());

	}

	@SuppressWarnings("unchecked")
	public SimpleHashMap() {
		load = 0.75;
		capacity = 16;
		size = 0;
		table = (Entry<K, V>[]) new Entry[capacity];
	}

	@SuppressWarnings("unchecked")
	public SimpleHashMap(int capacity) {
		load = 0.75;
		this.capacity = capacity;
		size = 0;
		table = (Entry<K, V>[]) new Entry[capacity];
	}

	public String show() {
		int i = 0;
		StringBuilder sb = new StringBuilder();
		for (Entry<K, V> entry : table) {
			i++;
			sb.append(i);
			while (entry != null) {
				sb.append("        ");
				sb.append(entry.toString());
				entry = entry.next;
			}
			sb.append("\n");
		}
		return sb.toString();
	}

	@Override
	public V get(Object key) {
		Entry<K, V> temp = find(index((K) key), (K) key);
		if (temp != null) {
			return temp.getValue();
		}
		return null;
	}

	@Override
	public boolean isEmpty() {
		return size() == 0 ? true : false;
	}

	@Override
	public V put(K key, V value) {
		Entry<K, V> entry = new Entry<K, V>(key, value);

		if (table[index(key)] == null) {
			table[index(key)] = entry;
			size++;
		} else {
			entry = find(index(key), key);
			if (entry != null) {
				V oldValue = entry.getValue();
				entry.setValue(value);
				return oldValue;
			}
			entry = table[index(key)];
			while (entry.next != null) {
				entry = entry.next;
			}
			entry.next = new Entry<K, V>(key, value);
			size++;
		}
		if ((double) size > load * capacity) {
			rehash();
		}
		return null;
	}
	
	private int index(K key) { // returnerar det index som ska användas för nyckeln key
		return Math.abs(key.hashCode() % table.length);
	}

	private Entry<K, V> find(int index, K key) { // returnerar det Entry-par som har nyckeln key i listan som finns på
		Entry<K, V> temp = table[index]; // positionen index i tabellen
		while (temp != null) {
			if (temp.getKey().equals(key)) {
				return temp;
			}
			temp = temp.next;
		}
		return null;
	}

	private void rehash() {
		capacity = 2 * capacity;
		Entry<K, V>[] tempTable = (Entry<K, V>[]) new Entry[capacity];
		Entry<K, V>[] oldTable = table;
		table = tempTable;
		size = 0;

		for (int i = 0; i < oldTable.length; i++) {
			Entry<K, V> temp = oldTable[i];
			while (temp != null) {
				put(temp.getKey(), temp.getValue());
				temp = temp.next;
			}
		}
	}

	@Override
	public V remove(Object key) {
		if (!isEmpty()) {
			Entry<K, V> temp = find(index((K) key), (K) key);
			Entry<K, V> temp2 = table[index((K) key)];

			if (temp == null) {
				return null;
			}
			if (temp != null) {
				V value = temp.getValue();

				if (temp.getKey() == temp2.getKey()) {
					if (temp.next != null) {
						table[index((K) key)] = temp.next;
					} else {
						table[index((K) key)] = null;
					}
					size--;
					return value;
				}

				else {
					while (temp2.next != null) {
						if (temp2.next.getKey().equals(temp.getKey())) {
							temp2.next = temp.next;
							size--;
							return temp.getValue();
						} else {
							temp2 = temp2.next;
						}
					}
					return null;
				}
			}
		}
		return null;
	}

	@Override
	public int size() {
		return size;
	}



	/*
	 * public boolean equals(Object obj) { if (obj instanceOf Entry<K, V>) { return
	 * value == ((Entry<K, V>) obj).value); } else { return false; } }
	 */

	public static class Entry<K, V> implements Map.Entry<K, V> {
		private K key;
		private V value;
		private Entry<K, V> next;

		public Entry(K k, V v) {
			this.key = k;
			this.value = v;
			this.next = null;
		}

		@Override
		public K getKey() {
			return key;
		}

		@Override
		public V getValue() {
			return value;
		}

		@Override
		public V setValue(V value) {
			V temp = this.value;
			this.value = value;
			return temp;
		}

		public String toString() {
			return key + "=" + value;
		}

	}

}