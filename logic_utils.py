def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = max(100 - 10 * attempt_number, 10)
        return current_score + points
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score


def temperature_label(guess: int, secret: int, low: int, high: int):
    """Return a hot/cold hint based on how close the guess is to the secret."""
    ratio = abs(guess - secret) / max(high - low, 1)
    if ratio <= 0.05:
        return "🔥 Very hot!"
    if ratio <= 0.15:
        return "♨️ Warm"
    if ratio <= 0.35:
        return "🌤️ Cool"
    return "🧊 Cold"
