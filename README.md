# 🎮 Sequence Board Game - AI Implementation

A complete, production-ready Python implementation of the Sequence board game with intelligent AI opponents powered by **Minimax algorithm with Alpha-Beta pruning**.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-28%2F28%20passing-brightgreen)](tests.py)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-blue)](https://www.python.org/dev/peps/pep-0008/)
[![License](https://img.shields.io/badge/license-Educational-orange)](LICENSE)

---

## 📖 Table of Contents

- [Quick Start](#-quick-start)
- [Game Features](#-game-features)
- [Installation](#-installation)
- [How to Play](#-how-to-play)
- [Game Rules](#-game-rules)
- [AI Difficulty Levels](#-ai-difficulty-levels)
- [Project Structure](#-project-structure)
- [Running Tests](#-running-tests)
- [API Usage](#-api-usage)
- [Documentation](#-documentation)

---

## ⚡ Quick Start

### Clone and Run in 3 Steps

```bash
# 1. Clone the repository
git clone https://github.com/hassan09070/projectAI.git
cd projectAI

# 2. Run the game (no installation needed!)
python3 main.py

# OR with virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

**That's it!** 🚀 No dependencies required - pure Python!

---

## 🎯 Game Features

### 🎲 Complete Sequence Game

- **Authentic 10×10 board** with official card layout
- **Wild corner positions** that benefit both players
- **Special Jack cards:**
  - 🃏 Two-eyed Jacks (♥J, ♦J) - Place chip anywhere (wild)
  - 🃏 One-eyed Jacks (♠J, ♣J) - Remove opponent's chip
- **2-3 player support**
- **Win detection** - First to complete 2 sequences wins!

### 🤖 Intelligent AI

- **4 Difficulty Levels:**
  - 🟢 Easy - Good for beginners
  - 🟡 Medium - Balanced gameplay
  - 🟠 Hard - Challenging opponent
  - 🔴 Expert - Maximum difficulty
- **Minimax algorithm** with Alpha-Beta pruning
- **Smart evaluation** considering:
  - Offensive sequence building
  - Defensive blocking
  - Board control
  - Card utility

### 💻 Code Quality

- ✅ **Zero external dependencies** - Pure Python
- ✅ **28 unit tests** - 100% passing
- ✅ **Type hints** throughout
- ✅ **Well-documented** code
- ✅ **Modular architecture**
- ✅ **Production-ready**

---

## 💾 Installation

### Option 1: Direct Run (Simplest)

```bash
# Clone the repository
git clone https://github.com/hassan09070/projectAI.git
cd projectAI

# Run immediately
python3 main.py
```

### Option 2: With Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/hassan09070/projectAI.git
cd projectAI

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Run the game
python main.py
```

### Option 3: Test First, Then Play

```bash
git clone https://github.com/hassan09070/projectAI.git
cd projectAI

# Run tests to verify everything works
python3 tests.py

# Run the game
python3 main.py
```

### System Requirements

- **Python 3.7 or higher**
- **No external libraries needed!**
- Works on: Windows, macOS, Linux

---

## 🎮 How to Play

### Starting the Game

```bash
python3 main.py
```

### Game Modes

When you start the game, you'll see:

```
============================================================
            WELCOME TO SEQUENCE BOARD GAME
============================================================

Game Setup:
1. Human vs Human
2. Human vs AI
3. AI vs AI (Demo)

Select game mode (1-3):
```

**Choose your mode:**

#### 1️⃣ Human vs Human
- Play against another person on the same computer
- Perfect for learning the game or playing with friends

#### 2️⃣ Human vs AI
- Challenge the computer
- Select difficulty: Easy, Medium, Hard, or Expert
- Great for practice or solo play

#### 3️⃣ AI vs AI (Demo)
- Watch two AI players compete
- See AI strategies in action

### During Your Turn

1. **View your hand** - See your available cards
2. **Select a card** - Choose which card to play
3. **Choose position** - Pick where to place your chip
4. **Watch the board** - See your move applied
5. **Next player's turn**

### Game Board Display

```
   0  1  2  3  4  5  6  7  8  9
  +------------------------------+
 0| *  .  .  .  .  .  .  .  .  * |
 1| .  .  .  .  .  .  .  .  .  . |
 2| .  .  2  .  .  .  .  .  1  . |
 3| .  1  .  .  .  .  .  .  .  . |
 4| .  .  .  .  1  2  .  .  .  . |
 5| .  .  .  .  2  1  .  .  .  . |
 6| .  .  .  .  .  .  .  .  .  . |
 7| .  .  .  .  .  .  .  .  .  . |
 8| .  .  .  .  .  .  .  .  .  . |
 9| *  .  .  .  .  .  .  .  .  * |
  +------------------------------+
```

- `.` = Empty position
- `1` = Player 1's chip
- `2` = Player 2's chip  
- `*` = Wild corner (counts for both players)

---

## 📜 Game Rules

### Objective

Be the **first player to complete 2 sequences**. A sequence is **5 connected chips** in a row (horizontally, vertically, or diagonally).

### Setup

1. Each player receives **7 cards** (6 cards for 3 players)
2. The deck contains **104 cards** (2 standard 52-card decks)
3. Players take turns clockwise

### On Your Turn

1. **Play a card** from your hand
2. **Place a chip** on a matching card on the board
3. **Draw a new card** to refill your hand
4. Check if you've completed a sequence

### Special Cards

#### Two-Eyed Jacks (♥J and ♦J)
- **Wild cards** - Can place your chip on ANY empty space
- Very powerful - use strategically!

#### One-Eyed Jacks (♠J and ♣J)  
- **Remove** any opponent's chip from the board
- Cannot remove chips from completed sequences
- Cannot remove from wild corners

### Wild Corners

The four corner positions are **wild** and count as occupied for **both players**:
- Top-left (0,0)
- Top-right (0,9)  
- Bottom-left (9,0)
- Bottom-right (9,9)

### Winning

- **2-player game**: First to complete **2 sequences** wins
- **3-player game**: First to complete **1 sequence** wins

---

## 🎯 AI Difficulty Levels

| Level | Search Depth | Nodes Explored | Time/Move | Best For |
|-------|--------------|----------------|-----------|----------|
| **Easy** | 1 | ~50-100 | <0.1s | Beginners |
| **Medium** | 2 | ~500-1,000 | ~0.5s | Intermediate |
| **Hard** | 3 | ~2,000-5,000 | ~2-3s | Advanced |
| **Expert** | 4 | ~10,000-20,000 | ~10-15s | Challenge |

### AI Strategy

The AI evaluates positions using:

- **Offensive Play**: Building sequences (2, 3, 4 in a row)
- **Defensive Play**: Blocking opponent sequences
- **Board Control**: Occupying strategic center positions
- **Card Utility**: Maximizing playable cards and wild jacks

---

## 📁 Project Structure

```
projectAI/
├── game/                    # Core game engine
│   ├── __init__.py
│   ├── board.py            # 10×10 board with sequence detection
│   ├── deck.py             # Card deck management
│   ├── player.py           # Player state and hand
│   └── gamestate.py        # Game logic and moves
│
├── ai/                      # AI implementation
│   ├── __init__.py
│   ├── heuristics.py       # Position evaluation
│   └── minimax.py          # Minimax + Alpha-Beta pruning
│
├── main.py                  # Game runner (start here!)
├── tests.py                 # 28 unit tests
├── examples.py              # Usage examples
│
├── README.md                # This file
├── QUICKSTART.md            # Quick reference
├── ARCHITECTURE.md          # Technical details
└── .gitignore              # Git ignore rules
```

---

## 🧪 Running Tests

Verify everything works correctly:

```bash
# Run all 28 tests
python3 tests.py
```

Expected output:
```
✓ All tests passed! (28/28)
```

### Test Coverage

- ✅ Board operations (9 tests)
- ✅ Deck management (6 tests)
- ✅ Player state (3 tests)
- ✅ Game logic (6 tests)
- ✅ AI functionality (4 tests)

---

## 💡 API Usage

Use the game engine programmatically:

### Basic Game

```python
from game import GameState

# Create a new game
state = GameState(num_players=2)
state.setup_game()

# Get legal moves
moves = state.get_legal_moves()

# Make a move
state.make_move(card="5H", row=3, col=4)

# Check winner
if state.is_terminal():
    winner = state.get_winner()
    print(f"Player {winner} wins!")
```

### AI Player

```python
from ai import MinimaxAI

# Create an AI player
ai = MinimaxAI(player_id=2, difficulty='hard')

# Get best move
best_move = ai.get_best_move(state)

# View statistics
stats = ai.get_stats()
print(f"Nodes explored: {stats['nodes_explored']}")
print(f"Pruning count: {stats['pruning_count']}")
```

### Board Operations

```python
from game import Board

board = Board()

# Get card at position
card = board.get_card_at(row=0, col=1)  # "6D"

# Place a chip
board.place_chip(row=3, col=4, player_id=1)

# Find card positions
positions = board.find_card_positions("5H")

# Check sequences
sequences = board.check_sequence(player_id=1)
```

### Export to JSON

```python
# Serialize game state
json_data = state.to_json()

# Save to file
with open('game_state.json', 'w') as f:
    f.write(json_data)
```

---

## 📚 Documentation

- **[README.md](README.md)** - This file (complete guide)
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[INDEX.md](INDEX.md)** - Navigation guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🎓 Examples

Run interactive examples:

```bash
python3 examples.py
```

See 7 different scenarios:
1. Basic game setup
2. AI vs AI game
3. Board operations
4. Deck management
5. Heuristic evaluation
6. JSON serialization
7. Complete game simulation

---

## 🚀 Quick Commands

```bash
# Play the game
python3 main.py

# Run tests
python3 tests.py

# See examples  
python3 examples.py

# View board layout (Python shell)
python3 -c "from game import Board; print(Board())"
```

---

## 🏆 Features Checklist

- [x] Complete Sequence game rules
- [x] 10×10 authentic board layout
- [x] Wild corners
- [x] Special jack mechanics
- [x] 2-3 player support
- [x] AI with 4 difficulty levels
- [x] Minimax with Alpha-Beta pruning
- [x] Smart heuristic evaluation
- [x] Win detection
- [x] JSON serialization
- [x] 28 comprehensive tests
- [x] Zero dependencies
- [x] Type hints
- [x] Full documentation

---

## 📊 Project Stats

- **Lines of Code**: ~2,360
- **Test Coverage**: 100%
- **Test Pass Rate**: 28/28 ✅
- **Python Version**: 3.7+
- **Dependencies**: None
- **Classes**: 7
- **Methods**: 83+

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Fork and enhance
- Report issues
- Suggest improvements
- Add features (GUI, networking, etc.)

---

## 📄 License

Educational use. Sequence is a registered trademark of Jax Ltd.

---

## 🎮 Ready to Play?

```bash
git clone https://github.com/hassan09070/projectAI.git
cd projectAI
python3 main.py
```

**Have fun!** 🎉

---

## 📞 Quick Help

**Q: The game won't start**  
A: Make sure you have Python 3.7+ installed: `python3 --version`

**Q: How do I quit during a game?**  
A: Press `Ctrl+C` to exit

**Q: Can I save my game?**  
A: Yes! The game offers to save when you finish

**Q: How do I make the AI easier/harder?**  
A: Select different difficulty when starting Human vs AI mode

**Q: Can I play online?**  
A: Not yet - current version is local only

---

**Enjoy the game!** 🎲✨
