from core.exceptions import InvalidKeyError

GRID_SIZE = 5


def encrypt(plaintext: str, key: str) -> str:
    grid = _build_grid(key)
    digraphs = _prepare_digraphs(plaintext)
    return "".join(_process_digraph(a, b, grid, encrypt_mode=True) for a, b in digraphs)


def decrypt(ciphertext: str, key: str) -> str:
    grid = _build_grid(key)
    if len(ciphertext) % 2 != 0:
        raise InvalidKeyError("Ciphertext length must be even for Playfair decryption.")
    digraphs = [(ciphertext[i], ciphertext[i + 1]) for i in range(0, len(ciphertext), 2)]
    return "".join(_process_digraph(a, b, grid, encrypt_mode=False) for a, b in digraphs)


def _build_grid(key: str) -> list[list[str]]:
    if not key or not key.isalpha():
        raise InvalidKeyError("Key must be a non-empty alphabetic string.")

    key = key.upper().replace("J", "I")
    seen = set()
    letters = []
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            letters.append(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # no J
        if char not in seen:
            seen.add(char)
            letters.append(char)

    return [letters[i:i + GRID_SIZE] for i in range(0, 25, GRID_SIZE)]


def _prepare_digraphs(text: str) -> list[tuple[str, str]]:
    letters = [c.upper().replace("J", "I") for c in text if c.isalpha()]
    digraphs = []
    i = 0
    while i < len(letters):
        a = letters[i]
        b = letters[i + 1] if i + 1 < len(letters) else "X"
        if a == b:
            digraphs.append((a, "X"))
            i += 1
        else:
            digraphs.append((a, b))
            i += 2
    return digraphs


def _find_position(grid: list[list[str]], char: str) -> tuple[int, int]:
    for row_idx, row in enumerate(grid):
        if char in row:
            return row_idx, row.index(char)
    raise InvalidKeyError(f"Character '{char}' not found in Playfair grid.")


def _process_digraph(a: str, b: str, grid: list[list[str]], encrypt_mode: bool) -> str:
    row_a, col_a = _find_position(grid, a)
    row_b, col_b = _find_position(grid, b)
    shift = 1 if encrypt_mode else -1

    if row_a == row_b:
        return grid[row_a][(col_a + shift) % GRID_SIZE] + grid[row_b][(col_b + shift) % GRID_SIZE]
    elif col_a == col_b:
        return grid[(row_a + shift) % GRID_SIZE][col_a] + grid[(row_b + shift) % GRID_SIZE][col_b]
    else:
        return grid[row_a][col_b] + grid[row_b][col_a]