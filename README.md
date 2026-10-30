# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects "Normal" difficulty (range 1-100) and enters a guess of 40
2. Game returns "Too Low" with the hint "Go Higher!" (this now points correctly at the right direction after the fix)
3. User enters a guess of 70, and the game shows "Too High with "Go Lower!"
4. Score updates by -5 for each wrong guess, consistently regardless of the attempt number
5. User enters the correct secret number, showing "Win", and awarding a score reflecting how few attempts were used, and displays a ballon celebration

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0 -- d:\CODEPATH\A110\ai110-module1show-gameglitchinvestigator-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\CODEPATH\A110\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 8 items

tests/test_game_logic.py::test_winning_guess PASSED                                                                                                                       [ 12%] 
tests/test_game_logic.py::test_guess_too_high PASSED                                                                                                                      [ 25%] 
tests/test_game_logic.py::test_guess_too_low PASSED                                                                                                                       [ 37%] 
tests/test_game_logic.py::test_score_awards_more_for_earlier_win PASSED                                                                                                   [ 50%] 
tests/test_game_logic.py::test_parse_guess_accepts_negative_number PASSED                                                                                                 [ 62%] 
tests/test_game_logic.py::test_parse_guess_truncates_decimal_input PASSED                                                                                                 [ 75%] 
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_text PASSED                                                                                                [ 87%] 
tests/test_game_logic.py::test_parse_guess_handles_extremely_large_number PASSED                                                                                          [100%] 

============================================================================== 8 passed in 0.03s ===============================================================================
```

## 🚀 Stretch Features

- [x] Challenge 1
- [x] Challenge 2
- [x] Challenge 3
- [x] Challenge 4 - Added a Hot/Cold temperature hint (`temperature_label` in `logic_utils.py`) shown as a caption under the Too High/Too Low warning in `app.py`. It scales distance-to-secret against the difficulty's range so "Hot" means the same relative closeness on Easy and Hard. Also added a live "Guess History" list in the sidebar (`app.py`, rendered from `st.session_state.history`) so players can see their past guesses without digging into Developer Debug Info.
