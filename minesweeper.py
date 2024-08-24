import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1: Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Step 2: Mark the cell as safe
        self.mark_safe(cell)

        # Step 3: Add a new sentence to the AI's knowledge base
        # Find all neighboring cells of the given cell
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Only add cells that are within bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # Filter out cells that are already known to be safe or mines
        cells = set()
        count_cpy = copy.deepcopy(count)

        for cl in neighbors:
            if cl in self.mines:
                count_cpy -= 1
            if cl not in self.mines | self.safes:
                cells.add(cl)  # only add cells that are of unknown state

        # Add the new sentence
        new_sentence = Sentence(cells, count_cpy)
        if new_sentence not in self.knowledge and len(new_sentence.cells) > 0:
            self.knowledge.append(new_sentence)

        # Step 4: Mark any additional cells as safe or as mines
        self.update_knowledge()

        # Step 5: Infer new sentences
        self.infer_new_sentences()

    def infer_new_sentences(self):
        """
        Infers new sentences by comparing existing sentences in the knowledge base.
        """
        new_sentences = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 != s2 and s1.cells and s2.cells:
                    # If one sentence is a subset of the other
                    if s1.cells.issubset(s2.cells):
                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count
                        if new_cells and new_count >= 0:
                            new_sentence = Sentence(new_cells, new_count)

                            if new_sentence not in self.knowledge:
                                new_sentences.append(new_sentence)

        # Add newly inferred sentences to the knowledge base
        self.knowledge.extend(new_sentences)

        # Update knowledge base with any new information
        self.update_knowledge()

    def update_knowledge(self):
        """
        Updates the AI's knowledge base by marking known mines and safes.
        """
        changed = True
        while changed:
            changed = False

            # Collect cells to mark as mines and safes
            known_mines = set()
            known_safes = set()

            for sentence in self.knowledge:
                known_mines |= sentence.known_mines()
                known_safes |= sentence.known_safes()

            # Mark any new mines and safes
            for mine in known_mines:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    changed = True

            for safe in known_safes:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    changed = True

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes - self.moves_made:
            return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for (i, j) in range(self.width, self.height):
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return i, j
        return None




