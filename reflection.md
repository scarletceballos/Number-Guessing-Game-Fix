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
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
