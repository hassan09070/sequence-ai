# Sequence Game - Quick Start Guide

## Installation

No external dependencies required! Just Python 3.7+

```bash
cd sequence_game
```

## Run the Game

```bash
python main.py
```

## Project Structure

```
sequence_game/
├── game/                    # Core game engine
│   ├── board.py            # 10x10 board with card mapping
│   ├── deck.py             # 2x52 card deck management
│   ├── player.py           # Player state and hand
│   └── gamestate.py        # Game logic and moves
├── ai/                      # AI implementation
│   ├── heuristics.py       # Position evaluation
│   └── minimax.py          # Minimax with alpha-beta pruning
├── main.py                  # Game runner
├── examples.py              # Usage examples
├── tests.py                 # Unit tests
└── README.md                # Full documentation
```

## Quick Examples

### Run Tests

```bash
python tests.py
```

All 28 tests should pass ✓

### Run Example Scenarios

```bash
python examples.py
```

See various features in action.

### Play Human vs AI

```bash
python main.py
# Choose option 2
# Select difficulty (1-4)
```

### Programmatic Usage

```python
from game import GameState
from ai import MinimaxAI

# Create game
state = GameState(num_players=2)
state.setup_game()

# Create AI
ai = MinimaxAI(player_id=2, difficulty='medium')

# Get best move
move = ai.get_best_move(state)
state.apply_move(move)
```

## Features Checklist

✅ 10×10 Board with authentic card layout
✅ Wild corner positions
✅ Two-eyed Jacks (wild cards)
✅ One-eyed Jacks (remove opponent chip)
✅ Sequence detection (horizontal, vertical, diagonal)
✅ Full game state management
✅ Minimax AI with alpha-beta pruning
✅ Multiple difficulty levels
✅ Heuristic evaluation (offensive/defensive/control/utility)
✅ JSON serialization
✅ Complete test suite
✅ Clean OOP architecture

## AI Difficulty Levels

| Level  | Depth | Nodes Explored (avg) |
|--------|-------|---------------------|
| Easy   | 1     | ~50-100            |
| Medium | 2     | ~500-1000          |
| Hard   | 3     | ~2000-5000         |
| Expert | 4     | ~10000-20000       |

## Game Rules Summary

1. **Goal**: Create 2 sequences (5 connected chips)
2. **Wild Jacks (♥J, ♦J)**: Place anywhere
3. **Remove Jacks (♠J, ♣J)**: Remove opponent chip
4. **Corners**: Wild for both players
5. **Turn**: Play card → Place/remove chip → Draw new card

## Next Steps

- Read `README.md` for full documentation
- Run `examples.py` to see features
- Run `tests.py` to verify installation
- Run `main.py` to start playing!

Enjoy! 🎮
