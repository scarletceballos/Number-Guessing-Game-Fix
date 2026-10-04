# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude to add a Guess History feature to the sidebar that shows every guess I've made so far in the current game, in order.

**What did the agent do?**

Claude edited `app.py` to add a block that reads `st.session_state.history` (already being populated on every submit via `st.session_state.history.append(...)`) and renders it as a numbered list under a "Guess History" subheader in `st.sidebar`, placed right after the `history` session_state initializer so it always has data to read from before the rest of the page renders.

**What did you have to verify or fix manually?**

I ran the app with `streamlit run app.py` and played through a few guesses to confirm the sidebar list grows in the correct order and doesn't appear until at least one guess has been made. No manual code corrections were needed — the feature reused the existing `history` state rather than introducing anything new, so it worked as given.


---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number input | "Identify edge-case inputs that could break parse_guess, like negative numbers, decimals, or extremely large values, and generate pytest cases." | `test_parse_guess_accepts_negative_number` — asserts `parse_guess("-5")` returns `(True, -5, None)` | Yes | Nothing in `parse_guess` blocks a leading `-`, so a negative guess should parse cleanly as a valid int rather than erroring; this confirms that behavior is intentional, not accidental. |
| Decimal input | (same prompt as above) | `test_parse_guess_truncates_decimal_input` — asserts `parse_guess("50.9")` returns `(True, 50, None)` | Yes | `parse_guess` deliberately routes decimal strings through `int(float(raw))`, which truncates rather than rejects — worth locking in as expected behavior instead of a silent surprise. |
| Extremely large number | (same prompt as above) | `test_parse_guess_handles_extremely_large_number` — asserts `parse_guess("99999999999999999999")` returns `(True, 99999999999999999999, None)` | Yes | Python ints have no fixed size limit, but it's worth confirming nothing downstream (string formatting, Streamlit rendering) breaks on an unusually large value. |


---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Add professional docstrings to every function in logic_utils.py, then review the file for PEP 8 compliance and apply your suggestions.
```

**Linting output before:**

```
app.py:20:22: E203 whitespace before ','
app.py:20:23: E231 missing whitespace after ','
app.py:80:2: W291 trailing whitespace
app.py:82:5: E231 missing whitespace after ','
app.py:82:10: E231 missing whitespace after ','
app.py:93:80: E501 line too long (204 > 79 characters)
app.py:95:49: E231 missing whitespace after ','
app.py:123:33: W291 trailing whitespace
app.py:124:80: E501 line too long (163 > 79 characters)
app.py:130:80: E501 line too long (88 > 79 characters)
app.py:155:72: W292 no newline at end of file
```

**Changes applied:**

Added full docstrings to get_range_for_difficulty, parse_guess, check_guess, update_score, and temperature_label in logic_utils.py. (Describe here any specific flake8 warnings it flagged — e.g. line length, blank-line spacing, unused imports — and which ones you fixed.)

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

There's a bug in this check_guess function where the hint direction is backwards (a guess higher than the secret says "Go Higher!" instead of "Go Lower!"). What's wrong and how do I fix it?


| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude | ChatGPT |
| **Response summary** | Identified that the `if guess > secret` branch returns the message meant for the opposite case, and swapped the two return statements' messages so the direction matches the comparison. | Identified the same issue by tracing the conditional logic. When guess > secret, the guess is already higher than the secret, so the correct hint is "📉 Go LOWER!". When guess < secret, the correct hint is "📈 Go HIGHER!". The fix would be to swap the hint messages in the two corresponding return statements without changing the comparison conditions. |
| **More Pythonic?** | Fix was a direct, minimal swap with no added complexity |The expected solution is similarly Pythonic because it makes the smallest possible change to the existing function instead of unnecessarily rewriting the logic or adding new code.|
| **Clearer explanation?** | Explained *why* the direction was wrong by tracing through a concrete example (guess=60, secret=50) rather than just stating the fix | Provided a similarly clear explanation using a concrete example such as guess=60 and secret=50. The explanation would make it clear that 60 > 50 means the player needs to guess lower, while a guess below the secret requires a higher guess. |


**Which did you prefer and why?**
Both models landed on the identical fix and gave equally clear, example-driven explanations for this bug, there wasn't a meaningful difference in code quality or Pythonic style between them. Where Claude stood out for me wasn't the explanation itself but the workflow around it. As I was working in Claude Code directly in this project, Claude could run `check_guess()` against real inputs and show me the live before/after output, rather than me having to trust a description of what the code does. It designed a verification loop, propose a fix, run it, see the actual result and is the main reason I'd reach for Claude again for this kind of debugging task, even though ChatGPT's standalone diagnosis was just as correct.