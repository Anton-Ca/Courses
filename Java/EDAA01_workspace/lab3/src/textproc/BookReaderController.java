package textproc;

import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Event;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.KeyStroke;
import javax.swing.ListSelectionModel;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import javax.swing.text.html.ListView;

public class BookReaderController {
	// Attribut
	Set<String> set = new HashSet<String>();
	GeneralWordCounter Gen;
	ArrayList<String> astr = new ArrayList<String>();
	Scanner scan;
	Scanner scan2;
	JList<Map.Entry<String, Integer>> listView;

	public BookReaderController() {
		// Skapar ett fönster
		SwingUtilities.invokeLater(() -> {
			try {
				createWindow(Gen, "BookReader", 100, 300);
			} catch (FileNotFoundException e) {
				// Print Error
				System.out.println("FileNotFoundException" + e.getMessage());
				e.printStackTrace();
			}
		});
	}

	private void createGeneralWordCounter() throws FileNotFoundException {
		// Läser in text från nilsholg.txt och undantagsord.txt
		scan = new Scanner(new File("nilsholg.txt"));
		scan2 = new Scanner(new File("undantagsord.txt"));

		// Begränsar scanner-objekten
		scan.findWithinHorizon("\uFEFF", 1);
		scan.useDelimiter("(\\s|,|-|\\.|:|;|!|\\?|'|\\\")+");
		scan2.findWithinHorizon("\uFEFF", 1);
		scan2.useDelimiter("(\\s|-|\\.|:|;|!|\\?|'|\\\")+");

		// Läser in orden och lägger till dem i astr
		while (scan.hasNext()) {
			String word = scan.next().toLowerCase();
			astr.add(word);
		}

		// Lägger till undantagsorden i set
		while (scan2.hasNext()) {
			String word = scan2.next().toLowerCase();
			set.add(word);
		}

		// Close scanners
		scan.close();
		scan2.close();

		// Skapar en GeneralWordCounter med argument set och räknar orden i astr.
		Gen = new GeneralWordCounter(set);
		Gen.process(astr);

		// Skapar listmodellen och lägger in en samling Map.Entry objekt
		//SortedListModel<Map.Entry<String, Integer>> listModel = new SortedListModel<>(Gen.getWordList());

	}

	private void createWindow(GeneralWordCounter counter, String title, int width, int height)
			throws FileNotFoundException {
		createGeneralWordCounter();
		// Skapar en frame och panel.
		JFrame frame = new JFrame(title);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container pane = frame.getContentPane();
		// pane är en behållarkomponent till vilken de övriga komponenterna (listvy,
		// knappar etc.) ska läggas till.

		// Skapar listmodellen och lägger in en samling Map.Entry objekt
		SortedListModel<Map.Entry<String, Integer>> listModel = new SortedListModel<>(Gen.getWordList());

		// Skapar ett textfält
		JTextField textField = new JTextField(20);
		
		// Metoder för att sortera alfabetiskt och baserat på frekvens
		// Skapar actionlistener för knappen alphabetic
		JButton alphabetic = new JButton("Alphabetic");
		alphabetic.addActionListener(a -> listModel.sort((o1, o2) -> {
			return (o1.getKey().compareTo(o2.getKey()));
		}));

		// Skapar actionlistener för knappen frequency
		JButton frequency = new JButton("Frequency");
		frequency.addActionListener(c -> listModel.sort((o1, o2) -> {
			return o2.getValue().compareTo(o1.getValue());
		}));		
		
		// Skapar listvyn och knyter den till listmodellen
		listView = new JList<>(listModel);

		// Anger att man bara kan markera en rad i listvyn
		listView.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		
		// Skapar actionlistener för knappen frequency
		JButton find = new JButton("Find Word");
		find.addActionListener(b -> {
			boolean bol = false;
			for (int i = 0; i < listModel.getSize(); i++) {
				if(listModel.getElementAt(i).getKey().toLowerCase().trim().equals(textField.getText().toLowerCase().trim())) {
					listView.addSelectionInterval(i,i);
					listView.ensureIndexIsVisible(listView.getSelectedIndex());
					bol = true;
					// return: funkar här istället för boolean
				}
			}
			if(bol == false) {
				JOptionPane.showMessageDialog(frame, "The word was not found!");
			}
		});		
		
		// Knappen kan användas genom att trycka ENTER-knappen
		textField.addActionListener(find.getActionListeners()[0]);

		// Knyter listvyn till en scrollbar
		JScrollPane scrollPane = new JScrollPane(listView);
		scrollPane.setPreferredSize(new Dimension(200, 100));
		scrollPane.setBorder(new EmptyBorder(5, 10, 5, 10));

		// Skapar en JLabel med en border
		JLabel label1 = new JLabel(" ");
		label1.setBorder(new EmptyBorder(5, 10, 5, 10));

		// Scrollningspanel
		pane.add(scrollPane, BorderLayout.WEST);
		pane.add(label1, BorderLayout.SOUTH);

		// Lägger till elementen i panelen pane
		pane.add(alphabetic);
		pane.add(frequency);
		pane.add(label1);

		// Skapar en JPanel alla element 
		JPanel southPanel = new JPanel();
		JPanel centerPanel = new JPanel();
		JPanel northPanel = new JPanel();
		pane.add(southPanel, BorderLayout.SOUTH);
		pane.add(centerPanel, BorderLayout.CENTER);
		pane.add(northPanel, BorderLayout.NORTH);
		southPanel.add(alphabetic);
		southPanel.add(frequency);
		centerPanel.add(find);
		northPanel.add(textField);
		southPanel.setBorder(BorderFactory.createEmptyBorder(10, 15, 15, 10));
		centerPanel.setBorder(BorderFactory.createEmptyBorder(10, 15, 15, 10));
		
		// Makes the frame visible
		frame.pack();
		frame.setVisible(true);
	}
}