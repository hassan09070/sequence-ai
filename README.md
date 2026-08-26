# Sequence AI — a board game that fights back

A full-stack implementation of the **Sequence** board game with AI opponents that
actually think: **Minimax with Alpha-Beta pruning** over a custom heuristic, exploring
**20,000+ game states per move** at the highest difficulty.

> **Side note — project origin**
>
> Built as the semester project for an **undergraduate Artificial Intelligence course**
> at Habib University. I'd been playing Sequence around the same time and couldn't find
> any app or site with genuinely competitive opponents — so when the course asked for an
> AI project, the two collided. It started as pure-Python game logic with a Minimax
> opponent, and grew into a complete full-stack application.
>
> Built with my teammates **Muhammad Affan** and **Rohan**.

---

## The AI

Four difficulty levels, each a deeper Minimax search with Alpha-Beta pruning
([`ai/minimax.py`](ai/minimax.py)):

| Difficulty | Depth | Nodes explored* | Think time* |
|---|:--:|--:|--:|
| Easy | 1 | 14 | < 0.01 s |
| Medium | 2 | 54 | 0.01 s |
| Hard | 3 | 444 | 0.11 s |
| **Expert** | 4 | **23,173** | 6.5 s |

<sub>*Measured from the opening position of a 2-player game; varies with board state.
The node counter is built into the engine (`nodes_explored`), so you can reproduce this.</sub>

The evaluation function ([`ai/heuristics.py`](ai/heuristics.py)) scores four things:

- **Offense** — progress toward completed sequences (a 4-in-a-row with an open end is
  worth far more than two scattered pairs)
- **Defense** — detecting and blocking the opponent's developing sequences
- **Board control** — weighted center and near-corner positions
- **Card utility** — the value of what's still in hand, including two-eyed (wild) and
  one-eyed (remove) Jacks

Because Sequence deals hidden cards, this is Minimax over the *visible* state — the AI
plans against what it can see, which keeps the search honest and the game winnable.

## The stack

```
game/          Pure-Python Sequence engine — zero dependencies
  board.py       10×10 board, authentic card layout, sequence detection
  deck.py        104-card double deck, Jacks handled per official rules
  gamestate.py   Turn management, legal-move generation, win detection
ai/            Minimax + Alpha-Beta and the heuristic evaluator
backend/       FastAPI REST API wrapping the engine
frontend/      Next.js (TypeScript, Tailwind) — interactive 10×10 board
main.py        Play in the terminal — no install needed
tests.py       28 tests covering board, deck, state, and AI
```

The core game has **zero dependencies** — `main.py` runs on any Python 3.7+ without
installing anything. The web stack is layered on top, not baked in.

## Run it

**Terminal (instant):**

```bash
python3 main.py        # play against the AI in the terminal
python3 tests.py       # 28/28 passing
```

**Full stack:**

```bash
# backend
cd backend
pip install -r requirements.txt
cp .env.example .env
python run.py                    # FastAPI on :8000

# frontend (second terminal)
cd frontend
npm install
npm run dev                      # Next.js on :3000
```

Or both at once: `./start-fullstack.sh`

## Rules, briefly

Two teams take turns playing a card from hand and placing a chip on one of that card's
two board cells. Five chips in a row — any direction — is a *sequence*; first to two
sequences wins. Two-eyed Jacks place a chip anywhere; one-eyed Jacks remove an opponent's
chip (unless it's part of a completed sequence). The four corners are wild for everyone.

## Docs

- [`docs/architecture.md`](docs/architecture.md) — module design and data flow
- [`docs/architecture-diagram.md`](docs/architecture-diagram.md) — visual system map

## Authors

- [Hassan Shahzad](https://github.com/hassan09070)
- Muhammad Affan
- Rohan

MIT licensed — see [LICENSE](LICENSE).
