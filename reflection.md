# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran `streamlit run app.py`, the game looked fully playable — difficulty selector, a text box for guesses, a submit button — but the feedback it gave was actively wrong. Guessing above the secret number told me to go *higher* (the opposite of what I needed), and every other guess I submitted seemed to get judged by a different rule than the guess before it, as if the game were comparing numbers as text on some turns. The score also crept up oddly slowly even when I was guessing well. Confirmed by reading `app.py` and running its functions directly in a Python shell (see table below).

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| `check_guess(60, 50)` — guess of 60 against secret 50 | Outcome `"Too High"` with a message telling the player to go **lower** | Outcome `"Too High"` but the message says `"📈 Go HIGHER!"` — the hint direction is backwards | `('Too High', '📈 Go HIGHER!')` |
| `check_guess(9, "10")` — simulates an even-numbered attempt, where `app.py` silently converts the secret to a string before comparing | Outcome `"Too Low"` (9 is numerically less than 10) | Outcome `"Too High"` — because the secret was turned into a string, the comparison fell into `check_guess`'s `except TypeError` fallback, which compares `"9" > "10"` as **text**, and lexicographically `"9" > "10"` is `True` | `('Too High', '📈 Go HIGHER!')` |
| `update_score(0, "Win", 2)` — winning on the first real guess (attempt counter is already 2 due to an off-by-one in how attempts are counted) | Score should reflect a first-try win, e.g. `80` | Score comes out as `70` — the formula and the pre-incremented attempt counter combine to under-reward an early win | `70` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude (via Claude Code) for this entire project. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Claude proposed refactoring the four logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` into `logic_utils.py`, and removing the `except TypeError` string-comparison fallback in `check_guess` entirely, on the reasoning that once the secret is never stringified, that fallback path becomes dead code that only hides bugs. I accepted this as written because I verified it: after removing it, `pytest -v` still passed on all existing and new tests, and manually playing the game through several even-numbered attempts in `streamlit run app.py` showed correct High/Low hints with no crashes.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  - When Claude first analyzed the "secret becomes a string on even attempts" bug, it initially claimed this made the game "unwinnable on even attempts." I didn't accept that conclusion as-is — I asked Claude to actually run `check_guess(50, "50")` to verify it, and the real output showed the game still correctly resolves to "Win" in that case (because Python's `except TypeError` fallback converts both sides to strings, and `"50" == "50"` is still true). The bug was real, but its actual impact was narrower than first described: it only corrupts the High/Low *hint direction* on even attempts (via lexicographic instead of numeric comparison), not the ability to register a win. I had Claude correct the bug writeup in `reflection.md` section 1 to reflect the verified behavior rather than the first guess at it.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I considered a bug fixed only once two things were both true: the relevant pytest test passed, and I could reproduce the original failure condition live in `streamlit run app.py` and see the corrected behavior instead.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  - For the hint-inversion bug, I ran `pytest -v test_guess_too_high` and `test_guess_too_low`, which assert the message text contains "LOWER" or "HIGHER" matching the correct direction — these failed against the original code and passed after the fix. For the secret-stringification bug, I manually played through several even-numbered attempts in the live app and confirmed the High/Low hint now matches a plain numeric comparison every time, not just on odd attempts.
- Did AI help you design or understand any tests? How?
  - Claude helped design the pytest cases by proposing assertions that targeted the *shape* of the bug (e.g., checking the message text's direction word, not just the outcome label, since the outcome label alone could still read "Too High" even with a backwards message). I reviewed and ran every test myself before trusting it.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Streamlit reruns the entire script top-to-bottom every time you interact with a widget (click a button, type in a box) — it's not like a traditional app where only one event handler fires. That's why `st.session_state` exists: it's the one place that survives across reruns, so things like the secret number, attempt count, and score don't get reset to their initial values every time you click "Submit Guess." If you forget to guard a session_state initializer with `if "x" not in st.session_state`, you'd wipe it on every interaction instead of just once at the start.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

   - One habit I want to keep: verifying an AI's claim about a bug's impact by actually running the code, not just trusting the explanation — that's what caught the gap in the "unwinnable" claim above. One thing I'd do differently next time: write the reproduction test *before* asking for the fix, so I have an objective pass/fail signal the moment the fix lands instead of relying on manual play-testing first. This project changed how I think about AI-generated code: it's a fast first draft, not a verified one — every claim about what the code does needs its own check.
