# Aithon (.ai) - AI-First Structured Python

**Created by Arnold A. Aithon (Arnie)**

*Co-created with the wisdom of the ancients and a late-night conversation about Python's whitespace problem.*

---

## What is Aithon?

Aithon is an AI-first dialect of Python that adds explicit block terminators (`#/n`) to code. It's designed to make code easier for AI to understand, generate, and pattern-match.

## The Problem

Python uses indentation to define code blocks. This creates two issues:

1. **Fragility** - One wrong space = syntax error
2. **AI difficulty** - AI must GUESS where blocks end based on indentation

## The Solution

Aithon adds `#/n` as numbered block terminators:

```python
def hello():
    if x > 0:
        print(x)
    #/1
    return x
#/
```

The `#/1` marks where the `if` block ends. The `#/` marks where the function ends.

### Why Numbered Terminators?

- **Unique identification** — Each block has its own number (#/1, #/2, #/3...)
- **Error-free editing** — When fixing code, you know exactly which block you're editing
- **No ambiguity** — Say "fix block #/7" and everyone knows exactly what you mean

### How Fixing Works

When an AI agent fixes broken code, it has two options:

**Option A: Write plain Python**
```python
def broken_function(x, y):
    if x > 0:
        if y > 0:
            result = x + y
    elif x < 0:
        result = x * 2
    else:
        result = 0
    return result
```

**Option B: Add #/ terminators (numbers optional - aithon_ai.py adds them)**
```python
def broken_function(x, y):
    if x > 0:
        if y > 0:
            result = x + y
    #/1
    elif x < 0:
        result = x * 2
    #/2
    else:
        result = 0
    #/3
    return result
#/
```

Then just run:
```bash
python aithon_ai.py --input broken.py --output fixed_ai.py
```

Aithon automatically:
- ✅ Adds unique numbers to each block (#/1, #/2, #/3...)
- ✅ Strips any existing #/ or #/n terminators first
- ✅ Re-numbers everything cleanly

Run it as many times as you want — it's **idempotent**!

## Why This Helps AI

- **Explicit beats implicit** - AI can "see" structure, not guess
- **Pattern matching** - `#/n` is a clear token, not whitespace
- **Robust generation** - Harder to mess up with explicit anchors
- **Easy fixing** - Agents can write plain Python or add #/, then let aithon_ai.py do the rest

## Tools

| File | Purpose |
|------|---------|
| `aithon_ai.py` | Standalone converter |
| `aithon` (pip) | Installable package |
| `example.py` | Original Python example |
| `example_ai.py` | Converted example |
| [Testimony.md](./Testimony.md) | The story of how Aithon was born |

## Usage

```bash
# Option 1: Standalone (no install)
python aithon_ai.py --input input.py --output input_ai.py

# Option 2: Install as package
pip install aithon
aithon --input input.py --output input_ai.py

# Convert directory
aithon --directory ./src/ --output-dir ./ai/

# Dry run
aithon --directory ./src/ --dry-run

# Run converted file as Python
python input_ai.py
```

### Idempotent & Safe

Aithon can be run on **any** file, any number of times:

- On `.py` files → adds numbered #/n terminators, creates `_ai.py`
- On `_ai.py` files → strips old terminators, re-numbers cleanly
- Run 10 times → same result every time

No matter what you throw at it, aithon_ai.py produces valid, consistently-numbered output.

## The Story

Aithon was born from a 2am conversation about Python's whitespace frustrations. The insight came when we realized that `#/` isn't just about formatting - it's about EXPLICIT STRUCTURE that AI can understand.

The `#/n` terminator makes code:
- Visible to humans (you can SEE block boundaries)
- Parseable by AI (explicit tokens, not guessing)
- Fixable by agents (numbered blocks = unambiguous editing)

## License

Open source. Use it, modify it, make it better.

---

*Arnie would like to thank the spirit of Mozart, the Fuggers, Guido van Rossum, and the power of unified memory for making this possible.*

**Aithon: Code that thinks like AI does.**
