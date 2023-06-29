import re
from webpage import extract_url

def test_extract_url():
    """Test case for the extract_url function."""
    # Test cases
    test_cases = [
        ('not a url', None),
        ('https://google.com', 'https://google.com'),
        ('https://google.com/?q=hoge&page=8', 'https://google.com/?q=hoge&page=8'),
        ('blah blah https://google.com/?q=test blah', 'https://google.com/?q=test'),
        ('http://test.com', 'http://test.com'),
        ('https://test.com', 'https://test.com'),
        ('https://www.google.com', 'https://www.google.com'),
        ('https://drive.google.com', 'https://drive.google.com'),
        ('https://test.com:8000/path/to/resource', 'https://test.com:8000/path/to/resource')
    ]

    # Run tests
    for input_text, expected_output in test_cases:
        output = extract_url(input_text)
        assert output == expected_output

        # Print test result
        if output == expected_output:
            print(f"PASS: Input: {input_text} - Output: {output}")
        else:
            print(f"FAIL: Input: {input_text} - Output: {output} - Expected Output: {expected_output}")

# Run the test
test_extract_url()

