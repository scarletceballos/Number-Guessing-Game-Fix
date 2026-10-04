import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    temperature_label,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title(" Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off")

st.sidebar.header("SETTINGS")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts Allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: attempts now start at 0 (was 1)
# so first submitted guess is counted as attempt 1, not 2
# Also fixes update_score downstream
# which was under-sorcing early wins because of this being off by one

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if st.session_state.history:
    st.sidebar.subheader("Guess History")
    for i, past_guess in enumerate(st.session_state.history, start=1):
        st.sidebar.write(f"{i}, {past_guess}")


st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess")
with col2:
    new_game = st.button("New Game")
with col3:
    show_hint = st.checkbox("Show Hint", value=True)


if new_game:
    # FIX: New Game used to always redraw from random.randint(1, 100)
    # regardless of difficulty, and never reset score/status/history, so
    # replaying after a win/loss reused stale state and (since status
    # stayed "won"/"lost") immediately re-triggered the game-over screen.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.status = "playing"
    st.success("New Game Started")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again")
    else:
        st.error("Game Over. Start a new game to try again")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok or guess_int is None:
        st.session_state.history.append(raw_guess)
        st.error(err)
    elif not (low <= guess_int <= high):
        st.session_state.history.append(guess_int)
        st.error(f"Enter a number between {low} and {high}")
    else:
        st.session_state.history.append(guess_int)

        # FIX: Logic breaks here
        # secret used to be silently converted to a string every other
        # attempt, which broke the int comparison and forced a buggy
        # lexicographic string-comparison fallback
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)
            st.caption(temperature_label(
                guess_int, st.session_state.secret, low, high
            ))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You Won! The secret was {st.session_state.secret}. "
                f"Final Score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
