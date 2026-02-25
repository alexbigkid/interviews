"""Tests for string transformation operations."""

from src.string.transformations import (
    caesar_cipher_decode,
    caesar_cipher_encode,
    capitalize_words,
    compress_string,
    decompress_string,
    integer_to_string,
    remove_spaces,
    reverse_words,
    reverse_words_order,
    run_length_encoding,
    string_to_integer,
    to_lower_case,
    to_upper_case,
)


class TestToLowerCase:
    """Test to_lower_case function."""

    def test_mixed_case(self):
        """Test mixed case string."""
        assert to_lower_case("Hello World") == "hello world"

    def test_already_lowercase(self):
        """Test already lowercase string."""
        assert to_lower_case("hello") == "hello"

    def test_all_uppercase(self):
        """Test all uppercase string."""
        assert to_lower_case("HELLO") == "hello"

    def test_with_numbers(self):
        """Test string with numbers."""
        assert to_lower_case("Hello123") == "hello123"

    def test_with_special_chars(self):
        """Test string with special characters."""
        assert to_lower_case("Hello!@#") == "hello!@#"

    def test_empty_string(self):
        """Test empty string."""
        assert to_lower_case("") == ""


class TestToUpperCase:
    """Test to_upper_case function."""

    def test_mixed_case(self):
        """Test mixed case string."""
        assert to_upper_case("Hello World") == "HELLO WORLD"

    def test_already_uppercase(self):
        """Test already uppercase string."""
        assert to_upper_case("HELLO") == "HELLO"

    def test_all_lowercase(self):
        """Test all lowercase string."""
        assert to_upper_case("hello") == "HELLO"

    def test_with_numbers(self):
        """Test string with numbers."""
        assert to_upper_case("hello123") == "HELLO123"

    def test_empty_string(self):
        """Test empty string."""
        assert to_upper_case("") == ""


class TestCapitalizeWords:
    """Test capitalize_words function."""

    def test_normal_sentence(self):
        """Test normal sentence."""
        assert capitalize_words("hello world") == "Hello World"

    def test_already_capitalized(self):
        """Test already capitalized sentence."""
        assert capitalize_words("Hello World") == "Hello World"

    def test_multiple_spaces(self):
        """Test sentence with multiple spaces."""
        assert capitalize_words("hello  world") == "Hello  World"

    def test_single_word(self):
        """Test single word."""
        assert capitalize_words("hello") == "Hello"

    def test_empty_string(self):
        """Test empty string."""
        assert capitalize_words("") == ""

    def test_with_punctuation(self):
        """Test sentence with punctuation."""
        assert capitalize_words("hello, world!") == "Hello, World!"


class TestReverseWords:
    """Test reverse_words function."""

    def test_simple_sentence(self):
        """Test simple sentence."""
        assert reverse_words("hello world") == "olleh dlrow"

    def test_single_word(self):
        """Test single word."""
        assert reverse_words("hello") == "olleh"

    def test_empty_string(self):
        """Test empty string."""
        assert reverse_words("") == ""

    def test_multiple_spaces(self):
        """Test sentence with multiple spaces."""
        assert reverse_words("hello  world") == "olleh  dlrow"

    def test_with_punctuation(self):
        """Test sentence with punctuation."""
        assert reverse_words("hello, world!") == "olleh, dlrow!"


class TestReverseWordsOrder:
    """Test reverse_words_order function."""

    def test_simple_sentence(self):
        """Test simple sentence."""
        assert reverse_words_order("hello world") == "world hello"

    def test_three_words(self):
        """Test three words."""
        assert reverse_words_order("the quick brown") == "brown quick the"

    def test_single_word(self):
        """Test single word."""
        assert reverse_words_order("hello") == "hello"

    def test_empty_string(self):
        """Test empty string."""
        assert reverse_words_order("") == ""

    def test_extra_spaces(self):
        """Test extra spaces."""
        result = reverse_words_order("  hello   world  ")
        assert result.strip() == "world hello"

    def test_with_punctuation(self):
        """Test with punctuation."""
        result = reverse_words_order("hello, world!")
        assert result.strip() == "world! hello,"


class TestRemoveSpaces:
    """Test remove_spaces function."""

    def test_with_spaces(self):
        """Test with spaces."""
        assert remove_spaces("hello world") == "helloworld"

    def test_multiple_spaces(self):
        """Test multiple spaces."""
        assert remove_spaces("hello   world") == "helloworld"

    def test_leading_trailing_spaces(self):
        """Test leading and trailing spaces."""
        assert remove_spaces("  hello world  ") == "helloworld"

    def test_no_spaces(self):
        """Test no spaces."""
        assert remove_spaces("hello") == "hello"

    def test_only_spaces(self):
        """Test only spaces."""
        assert remove_spaces("   ") == ""

    def test_empty_string(self):
        """Test empty string."""
        assert remove_spaces("") == ""


class TestCompressString:
    """Test compress_string function."""

    def test_simple_compression(self):
        """Test simple compression."""
        assert compress_string("aabcccccaaa") == "a2b1c5a3"

    def test_no_compression_benefit(self):
        """Test no compression benefit."""
        result = compress_string("abcdef")
        assert result == "abcdef"  # Original string if compression doesn't help

    def test_single_character(self):
        """Test single character string."""
        assert compress_string("a") == "a"

    def test_three_different_character(self):
        """Test 3 different character string."""
        assert compress_string("abc") == "abc"

    def test_empty_string(self):
        """Test empty string."""
        assert compress_string("") == ""

    def test_all_same_character(self):
        """Test string with all same characters."""
        assert compress_string("aaaa") == "a4"


class TestDecompressString:
    """Test decompress_string function."""

    def test_simple_decompression(self):
        """Test simple decompression."""
        assert decompress_string("a2b1c5a3") == "aabcccccaaa"

    def test_single_characters(self):
        """Test single character counts."""
        assert decompress_string("a1b1c1") == "abc"

    def test_large_numbers(self):
        """Test large counts."""
        assert decompress_string("a10") == "aaaaaaaaaa"

    def test_empty_string(self):
        """Test empty string."""
        assert decompress_string("") == ""

    def test_no_compression_format(self):
        """Test string not in compression format."""
        # If input is not in compressed format, should handle gracefully
        result = decompress_string("abc")
        assert isinstance(result, str)


class TestStringToInteger:
    """Test string_to_integer function."""

    def test_positive_number(self):
        """Test positive number."""
        assert string_to_integer("123") == 123

    def test_negative_number(self):
        """Test negative number."""
        assert string_to_integer("-123") == -123

    def test_with_leading_spaces(self):
        """Test with leading spaces."""
        assert string_to_integer("  123") == 123

    def test_with_trailing_characters(self):
        """Test with trailing non-numeric characters."""
        assert string_to_integer("123abc") == 123

    def test_zero(self):
        """Test zero."""
        assert string_to_integer("0") == 0

    def test_overflow(self):
        """Test very large number."""
        result = string_to_integer("99999999999999999999")
        assert isinstance(result, int)

    def test_invalid_string(self):
        """Test invalid string."""
        assert string_to_integer("abc") == 0


class TestIntegerToString:
    """Test integer_to_string function."""

    def test_positive_number(self):
        """Test positive number."""
        assert integer_to_string(123) == "123"

    def test_negative_number(self):
        """Test negative number."""
        assert integer_to_string(-123) == "-123"

    def test_zero(self):
        """Test zero."""
        assert integer_to_string(0) == "0"

    def test_large_number(self):
        """Test large number."""
        assert integer_to_string(999999) == "999999"


class TestCaesarCipherEncode:
    """Test caesar_cipher_encode function."""

    def test_simple_shift(self):
        """Test simple shift."""
        assert caesar_cipher_encode("abc", 1) == "bcd"

    def test_wrap_around(self):
        """Test wrap around from z to a."""
        assert caesar_cipher_encode("xyz", 1) == "yza"

    def test_preserve_case(self):
        """Test preserving case."""
        assert caesar_cipher_encode("ABC", 1) == "BCD"

    def test_preserve_non_letters(self):
        """Test preserving non-letter characters."""
        assert caesar_cipher_encode("a1b2c3", 1) == "b1c2d3"

    def test_zero_shift(self):
        """Test zero shift."""
        assert caesar_cipher_encode("hello", 0) == "hello"

    def test_large_shift(self):
        """Test large shift."""
        assert caesar_cipher_encode("abc", 26) == "abc"


class TestCaesarCipherDecode:
    """Test caesar_cipher_decode function."""

    def test_simple_decode(self):
        """Test simple decode."""
        assert caesar_cipher_decode("bcd", 1) == "abc"

    def test_wrap_around(self):
        """Test wrap around from a to z."""
        assert caesar_cipher_decode("abc", 1) == "zab"

    def test_preserve_case(self):
        """Test preserving case."""
        assert caesar_cipher_decode("BCD", 1) == "ABC"

    def test_roundtrip(self):
        """Test encoding followed by decoding returns original."""
        original = "Hello World!"
        encoded = caesar_cipher_encode(original, 13)
        decoded = caesar_cipher_decode(encoded, 13)
        assert decoded == original


class TestRunLengthEncoding:
    """Test run_length_encoding function."""

    def test_simple_encoding(self):
        """Test simple encoding."""
        assert run_length_encoding("aaabbcccc") == "3a2b4c"

    def test_no_repeats(self):
        """Test string with no repeating characters."""
        assert run_length_encoding("abcd") == "1a1b1c1d"

    def test_single_character(self):
        """Test single character string."""
        assert run_length_encoding("a") == "1a"

    def test_empty_string(self):
        """Test empty string."""
        assert run_length_encoding("") == ""

    def test_all_same(self):
        """Test string with all same characters."""
        assert run_length_encoding("aaaa") == "4a"
