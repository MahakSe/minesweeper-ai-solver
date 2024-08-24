# Minesweeper AI Solver

This project implements an AI agent that can intelligently play the classic Minesweeper game. The AI uses knowledge representation and propositional logic to infer safe moves and identify mines on the board.

## Project Overview

Minesweeper is a puzzle game where players must identify hidden mines on a grid without triggering them. The goal is to flag all mines while revealing all safe cells. This project builds an AI agent that can play Minesweeper by making informed decisions based on the information provided by the board.

### Key Concepts:
- **Propositional Logic**: The AI represents each cell as a propositional variable that is either a mine or not. It uses logical inferences to deduce safe cells and mines.
- **Knowledge Representation**: The AI maintains a knowledge base of logical sentences that represent information about the board, allowing it to make informed moves.
- **Inference**: By analyzing the relationships between cells and their neighbors, the AI can infer new information and make educated guesses about which cells are safe.

## Files

- **runner.py**: Contains the graphical interface and game logic. You can run this file to play Minesweeper, either manually or with the AI.
- **minesweeper.py**: Contains the core logic of the game and the AI agent. This is where the Minesweeper class, Sentence class, and MinesweeperAI class are implemented.

## Requirements

- Python 3.12
- `pygame` library

Install the required dependencies by running:
```bash
pip3 install -r requirements.txt
