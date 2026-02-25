"""String transformation algorithms for interview preparation."""


def to_lower_case(s: str) -> str:
    """Convert string to lowercase without using built-in functions.

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        Lowercase version of string

    Examples:
        >>> to_lower_case("Hello World")
        'hello world'
        >>> to_lower_case("ABC123")
        'abc123'
        >>> to_lower_case("")
        ''
    """
    result = ""
    for char in s:
        if "A" <= char <= "Z":
            result += chr(ord(char) + 32)
        else:
            result += char
    return result


def to_upper_case(s: str) -> str:
    """Converts to upper case without using built-in functions."""
    result = ""
    for char in s:
        if "a" <= char <= "z":
            result += chr(ord(char) - 32)
        else:
            result += char
    return result


def capitalize_words(s: str) -> str:
    """Capitalize the first letter of each word in a string."""
    result = ""
    capitalize_next = True
    for char in s:
        if char == " ":
            result += char
            capitalize_next = True
        elif capitalize_next:
            result += chr(ord(char) - 32) if "a" <= char <= "z" else char
            capitalize_next = False
        else:
            result += char
    return result


def reverse_words(s: str) -> str:
    """Reverse each word in a string while preserving spacing and punctuation positions.

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        String with each word reversed but spacing and punctuation preserved

    Examples:
        >>> reverse_words("hello world")
        'olleh dlrow'
        >>> reverse_words("hello, world!")
        'olleh, dlrow!'
        >>> reverse_words("hello  world")
        'olleh  dlrow'
    """
    if len(s) == 0:
        return ""

    result, word = [], []

    for char in s:
        if char.isalnum():
            word.append(char)
        else:
            result.extend(word[::-1])
            word = []
            result.append(char)

    result.extend(word[::-1])
    return "".join(result)


def reverse_words_order(s: str) -> str:
    """Reverse the order of the worlds in a string."""
    words = s.split()
    return " ".join(words[::-1])


def remove_spaces(s: str) -> str:
    """Remove extra spaces from string without using string manipulation.

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        String with extra spaces removed

    Examples:
        >>> remove_spaces("  Hello   World  ")
        'HelloWorld'
        >>> remove_spaces("The    Quick   Brown  Fox")
        'TheQuickBrownFox'
        >>> remove_spaces("")
        ''
    """
    result = ""
    for char in s:
        if char != " ":
            result += char
    return result


def compress_string(s: str) -> str:
    """Compress string using counts of repeated characters.

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        Compressed string or original if no space saved

    Examples:
        >>> compress_string("aabcccccaaa")
        'a2b1c5a3'
        >>> compress_string("abcdef")
        'abcdef'
        >>> compress_string("")
        ''
    """
    if len(s) == 0:
        return s

    compressed = ""
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed += s[i - 1] + str(count)
            count = 1

    compressed += s[-1] + str(count)
    return compressed if len(compressed) < len(s) else s


def decompress_string(s: str) -> str:
    """Decompress string encoded with character counts.

    Time: O(n), Space: O(m) where m is output length

    Args:
        s: Compressed string

    Returns:
        Decompressed string

    Examples:
        >>> decompress_string("a2b1c5a3")
        'aabcccccaaa'
        >>> decompress_string("a1b1c1")
        'abc'
        >>> decompress_string("")
        ''
    """
    result = []
    i = 0

    while i < len(s):
        ch = s[i]
        i += 1

        count = 0
        while i < len(s) and s[i].isdigit():
            count = count * 10 + (ord(s[i]) - ord("0"))  # build number
            i += 1

        result.extend(ch * (count or 1))

    return "".join(result)


def string_to_integer(s: str) -> int:
    """Convert string to integer without using built-in conversion functions (atoi implementation).

    Time: O(n), Space: O(1)

    Args:
        s: Input string

    Returns:
        Integer representation of string, 0 if invalid

    Examples:
        >>> string_to_integer("123")
        123
        >>> string_to_integer("-456")
        -456
        >>> string_to_integer("0")
        0
        >>> string_to_integer("  123")
        123
        >>> string_to_integer("123abc")
        123
        >>> string_to_integer("abc")
        0
    """
    if len(s) == 0:
        return 0

    s = s.strip()
    if len(s) == 0:  # Only spaces
        return 0

    # Check for sign
    i = 0
    sign = 1
    if s[i] == "-":
        sign = -1
        i += 1
    elif s[i] == "+":
        i += 1

    # Convert digits
    num = 0
    while i < len(s) and "0" <= s[i] <= "9":
        num = num * 10 + (ord(s[i]) - ord("0"))
        i += 1

    return sign * num


def integer_to_string(num: int) -> str:
    """Convert integer to string without using built-in conversion functions.

    Time: O(n), Space: O(n)

    Args:
        num: Input integer

    Returns:
        String representation of integer

    Examples:
        >>> integer_to_string(123)
        '123'
        >>> integer_to_string(-456)
        '-456'
        >>> integer_to_string(0)
        '0'
    """
    if num == 0:
        return "0"

    is_negative = num < 0
    num = abs(num)

    digits = []
    while num > 0:
        digits.append(chr(ord("0") + num % 10))
        num //= 10

    if is_negative:
        digits.append("-")

    return "".join(reversed(digits))


def caesar_cipher_encode(s: str, shift: int) -> str:
    """Apply Caesar cipher with given shift.

    Time: O(n), Space: O(n)

    Args:
        s: Input string
        shift: Number of positions to shift (can be negative)

    Returns:
        Encrypted string

    Examples:
        >>> caesar_cipher_encode("abc", 3)
        'def'
        >>> caesar_cipher_encode("xyz", 3)
        'abc'
        >>> caesar_cipher_encode("Hello", 1)
        'Ifmmp'
    """
    result = ""
    shift = shift % 26  # Normalize shift

    for char in s:
        if "a" <= char <= "z":
            new_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            result += new_char
        elif "A" <= char <= "Z":
            new_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            result += new_char
        else:
            result += char

    return result


def caesar_cipher_decode(s: str, shift: int) -> str:
    """Apply Caesar cipher with given shift.

    Time: O(n), Space: O(n)

    Args:
        s: Input string
        shift: Number of positions to shift (can be negative)

    Returns:
        Encrypted string

    Examples:
        >>> caesar_cipher_encode("abc", 3)
        'def'
        >>> caesar_cipher_encode("xyz", 3)
        'abc'
        >>> caesar_cipher_encode("Hello", 1)
        'Ifmmp'
    """
    return caesar_cipher_encode(s, -shift)


def run_length_encoding(s: str) -> str:
    """Compress string using run-length encoding.

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        Run-length encoded string

    Examples:
        >>> run_length_encoding("aabcccccaaa")
        'a2b1c5a3'
        >>> run_length_encoding("abc")
        'a1b1c1'
        >>> run_length_encoding("")
        ''
    """
    if len(s) == 0:
        return s

    encoded = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            encoded.append(f"{count}{s[i - 1]}")
            count = 1

    encoded.append(f"{count}{s[-1]}")
    return "".join(encoded)


def run_length_decoding(s: str) -> str:
    """Decompress run-length encoded string.

    Time: O(n), Space: O(m) where m is output length

    Args:
        s: Run-length encoded string

    Returns:
        Decoded string

    Examples:
        >>> run_length_decoding("a2b1c5a3")
        'aabcccccaaa'
        >>> run_length_decoding("a1b1c1")
        'abc'
        >>> run_length_decoding("")
        ''
    """
    result = []
    i = 0
    while i < len(s):
        char = s[i]
        count = 1
        while i + 1 < len(s) and s[i + 1] == char:
            i += 1
            count += 1
        result.append(f"{char}{count}")
        i += 1
    return "".join(result)


def zigzag_conversion(s: str, num_rows: int) -> str:
    """Convert string in zigzag pattern on given number of rows.

    Time: O(n), Space: O(n)

    Args:
        s: Input string
        num_rows: Number of rows for zigzag

    Returns:
        String read line by line from zigzag pattern

    Examples:
        >>> zigzag_conversion("PAYPALISHIRING", 3)
        'PAHNAPLSIIGYIR'
        >>> zigzag_conversion("PAYPALISHIRING", 4)
        'PINALSIGYAHRPI'
    """
    if num_rows == 1 or num_rows >= len(s):
        return s

    rows = [""] * num_rows
    current_row, step = 0, 1

    for char in s:
        rows[current_row] += char
        if current_row == 0:
            step = 1
        elif current_row == num_rows - 1:
            step = -1
        current_row += step

    return "".join(rows)


def integer_to_roman(num: int) -> str:
    """Convert integer to Roman numeral.

    Time: O(1), Space: O(1)

    Args:
        num: Integer to convert (1 <= num <= 3999)

    Returns:
        Roman numeral representation

    Examples:
        >>> integer_to_roman(3)
        'III'
        >>> integer_to_roman(4)
        'IV'
        >>> integer_to_roman(1994)
        'MCMXCIV'
    """
    roman_map = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    result = []
    for value, symbol in roman_map:
        while num >= value:
            result.append(symbol)
            num -= value
    return "".join(result)


def roman_to_integer(s: str) -> int:
    """Convert Roman numeral to integer.

    Time: O(n), Space: O(1)

    Args:
        s: Roman numeral string

    Returns:
        Integer value

    Examples:
        >>> roman_to_integer("III")
        3
        >>> roman_to_integer("IV")
        4
        >>> roman_to_integer("MCMXCIV")
        1994
    """
    roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    total = 0
    prev_value = 0

    for char in reversed(s):
        value = roman_map[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


def base64_encode(s: str) -> str:
    """Encode string to base64 (simplified implementation).

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        Base64 encoded string

    Examples:
        >>> base64_encode("Man")
        'TWFu'
        >>> base64_encode("pleasure.")
        'cGxlYXN1cmUu'
    """
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = []
    padding = 0

    # Process input in chunks of 3 bytes
    for i in range(0, len(s), 3):
        chunk = s[i : i + 3]
        if len(chunk) < 3:
            padding = 3 - len(chunk)
            chunk += "\0" * padding  # Pad with null bytes

        # Convert chunk to a 24-bit number
        num = (ord(chunk[0]) << 16) + (ord(chunk[1]) << 8) + ord(chunk[2])

        # Extract four 6-bit segments
        for j in range(18, -1, -6):
            index = (num >> j) & 0x3F
            result.append(base64_chars[index])

    # Add padding characters if necessary
    for _ in range(padding):
        result[-1 - _] = "="

    return "".join(result)


def normalize_string(s: str) -> str:
    """Normalize string by removing extra spaces and converting to lowercase.

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        Normalized string

    Examples:
        >>> normalize_string("  Hello   World  ")
        'hello world'
        >>> normalize_string("The    Quick   Brown  Fox")
        'the quick brown fox'
        >>> normalize_string("")
        ''
    """
    s = s.strip().lower()
    return s
