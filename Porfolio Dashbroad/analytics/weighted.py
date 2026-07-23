def weight(x: list, y: list) -> float:
    return sum(a * b for a, b in zip(x, y))