# 🔢 Finite Automata for Lexical Analysis

Hand-built finite-state automata in Python for recognizing and parsing numbers, lexing arithmetic expressions, and evaluating prefix expressions - completed as part of the Language Theory (Théorie des Langages) course at **Grenoble INP - Ensimag**.

## What it does

Starting from simple character-recognition automata, the project builds up to a small expression evaluator:

- **Number recognition**: automata accepting integers, point-floats (`3.14`), and exponent-floats (`1.5e3`, `2E-4`) - first as pure acceptors, then extended to compute the actual numeric value while parsing
- **Prefix expression evaluator** (`eval_exp`, `eval_exp_v2`): recursively evaluates arithmetic expressions in prefix notation (e.g. `+ 3 * 4 5` → `23`)
- **Lexer** (`LA_Lex`, `FA_Lex_w_token`): tokenizes input into numbers and operators/parentheses, laying the groundwork for a proper parser

Each automaton is implemented as a set of Python functions, one per state, mirroring how a state machine would be drawn on paper - each function reads the next character and transitions to the function representing the next state.

## Example

```python
>>> integer()  # reading "42"
(True, 42)

>>> pointfloat()  # reading "3.14"
(True, 3.14)
```

## Running it

```bash
python3 tp.py
```

Edit the `__main__` block to switch which automaton is tested (see comments in the file).

## Tech stack

Python
