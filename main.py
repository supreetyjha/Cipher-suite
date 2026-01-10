import string

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    # Decrypting is just encrypting with a negative shift
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if char.isalpha():
            # Handle uppercase and lowercase separately
            start = ord('A') if char.isupper() else ord('a')
            # The formula: (x + n) % 26
            new_char = chr(start + (ord(char) - start + shift) % 26)
            result += new_char
        else:
            # Step 4: Keep punctuation/spaces as they are
            result += char
    return result

def brute_force(text):
    print("\n--- Brute Force Results ---")
    for shift in range(1, 26):
        print(f"Shift {shift:02}: {caesar_cipher(text, shift, 'decrypt')}")

def analyze_frequency(text):
    text = text.lower()
    stats = {}
    for char in text:
        if char.isalpha():
            stats[char] = stats.get(char, 0) + 1
    
    print("\n--- Character Frequency Analysis ---")
    for char in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"{char[0]}: {char[1]}")

def main():
    print("Welcome to the Caesar Cipher Tool!")
    while True:
        choice = input("\nDo you want to (E)ncrypt, (D)ecrypt, (B)rute Force, or (Q)uit? ").upper()
        
        if choice == 'Q':
            break
            
        message = input("Enter your message: ")
        
        if choice == 'E':
            shift = int(input("Enter shift key (1-25): "))
            print(f"Result: {caesar_cipher(message, shift, 'encrypt')}")
        elif choice == 'D':
            shift = int(input("Enter shift key (1-25): "))
            print(f"Result: {caesar_cipher(message, shift, 'decrypt')}")
        elif choice == 'B':
            brute_force(message)
        
        analyze_frequency(message)

if __name__ == "__main__":
    main()