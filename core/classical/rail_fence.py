from core.exceptions import InvalidKeyError


def encrypt(plaintext: str, rails: int) -> str:
    _validate_rails(rails, plaintext)
    fence = [[] for _ in range(rails)]
    rail, direction = 0, 1

    for char in plaintext:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    return "".join("".join(row) for row in fence)


def decrypt(ciphertext: str, rails: int) -> str:
    _validate_rails(rails, ciphertext)
    pattern = _build_pattern(len(ciphertext), rails)

    counts = [pattern.count(r) for r in range(rails)]
    pointers = [0]
    for c in counts[:-1]:
        pointers.append(pointers[-1] + c)

    rail_chars = []
    cursor = 0
    for count in counts:
        rail_chars.append(list(ciphertext[cursor:cursor + count]))
        cursor += count

    result = []
    rail_positions = [0] * rails
    for rail in pattern:
        result.append(rail_chars[rail][rail_positions[rail]])
        rail_positions[rail] += 1

    return "".join(result)


def _validate_rails(rails: int, text: str) -> None:
    if rails < 2:
        raise InvalidKeyError("Number of rails must be at least 2.")
    if rails > max(len(text), 2):
        raise InvalidKeyError("Number of rails cannot exceed text length.")


def _build_pattern(length: int, rails: int) -> list[int]:
    pattern = []
    rail, direction = 0, 1
    for _ in range(length):
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return pattern