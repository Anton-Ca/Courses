package sudoku;

public class SudokuSolver {

	private int[][] sudoku;

	/** Skapar en matris som är 9 * 9 */

	public SudokuSolver() {
		sudoku = new int[9][9];
	}

	/** Scannar in de siffror som skrivits på sudokun av användaren */

	public void scanMatrix(OneLetterField[][] field) {
		for (int i = 0; i < 9; i++) {
			for (int j = 0; j < 9; j++) {
				if (field[i][j].getText().equals("")) {
					sudoku[i][j] = 0;
				} else {
					int z = Integer.parseInt(field[i][j].getText());
					sudoku[i][j] = z;

				}
			}
		}
	}

	/**
	 * Testar och ser om de siffror som skrivits in av användaren uppfyller
	 * reglerna
	 */

	public boolean testFile() {
		for (int i = 0; i < 9; i++) {
			for (int j = 0; j < 9; j++) {
				if (!checkRules(i, j)) {
					return true;
				}
			}
		}
		return false;
	}

	/** Returnerar innehållet av sudokun i en matris */

	public int[][] getSolved() {
		return sudoku;
	}

	/**
	 * Löser sudokun rekursivt,
	 * 
	 * @return
	 */

	public boolean solve(int row, int column) {

		if (row == 9) { // har vi kommit till rad 9 är vi klara (sista rutan)
			return true;
		}

		if (sudoku[row][column] == 0) {
			for (int x = 1; x <= 9; x++) {
				sudoku[row][column] = x;
				if (checkRules(row, column)) {
					if (column != 8) {
						if (solve(row, column + 1)) {
							return true;
						}
					} else {
						if (solve(row + 1, 0)) {  
							return true;
						}
					}
				}
			}
			sudoku[row][column] = 0;
			return false;

		} else {
			if (checkRules(row, column)) {
				if (column == 8) {
					if (solve(row + 1, 0)) {
						return true;
					}
				} else {
					if (solve(row, column + 1)) {
						return true;
					}

				}
			}
		}
		return false;
	}

	/**
	 * Undersöker om en specifik siffra uppfyller de regler som finns. Om så är
	 * fallet returneras true, annars returneras false
	 */

	private boolean checkRules(int r, int c) {
		for (int i = 0; i < 9; i++) {
			if (i != c) {
				if (sudoku[r][i] == sudoku[r][c]) {
					return false;
				}
			}
			if (i != r) {
				if (sudoku[i][c] == sudoku[r][c]) {
					return false;
				}
			}
		}

		int cc = 3 * (c / 3);
		int rr = 3 * (r / 3);

		for (int rad = rr; rad <= rr + 2; rad++) {
			for (int col = cc; col <= cc + 2; col++) {
				if (sudoku[rad][col] == sudoku[r][c] && rad != r && col != c) {
					return false;
				}
			}
		}
		return true;
	}

}
