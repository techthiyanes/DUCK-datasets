def is_good_float(ans : float, correct : float, tol : float = 0.01) -> bool:
    return abs(ans - correct) < tol

def is_good_latex(ans : str, correct : str) -> bool:
    correct = correct.replace("$", "")
    ans = ans.replace("$", "")
    if correct == ans:
        return True
    else:
        print(f"Correct: {correct}, Answer: {ans}")

