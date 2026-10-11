def feedback(code, guess):
    code = list(code)
    guess = list(guess)
    matched_code = [False] * len(code)
    matched_guess = [False] * len(guess)

    exact = 0
    for index, (code_symbol, guess_symbol) in enumerate(zip(code, guess)):
        if code_symbol == guess_symbol:
            matched_code[index] = True
            matched_guess[index] = True
            exact += 1

    partial = 0
    for guess_index, guess_symbol in enumerate(guess):
        if matched_guess[guess_index]:
            continue
        for code_index, code_symbol in enumerate(code):
            if not matched_code[code_index] and guess_symbol == code_symbol:
                matched_code[code_index] = True
                partial += 1
                break

    return exact, partial
