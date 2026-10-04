from logic_utils import check_guess, parse_guess, update_score


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_score_awards_more_for_earlier_win():
    first_try_score = update_score(0, "Win", 1)
    later_try_score = update_score(0, "Win", 5)
    assert first_try_score > later_try_score
    assert first_try_score == 90


# --- Edge cases (Challenge 1) ---

def test_parse_guess_accepts_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_truncates_decimal_input():
    ok, value, err = parse_guess("50.9")
    assert ok is True
    assert value == 50


def test_parse_guess_rejects_non_numeric_text():
    ok, value, err = parse_guess("banana")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_handles_extremely_large_number():
    ok, value, err = parse_guess("99999999999999999999")
    assert ok is True
    assert value == 99999999999999999999
