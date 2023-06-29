from typing import Dict, Optional
import random

language_map: Dict[str, Optional[str]] = {
    'javascript': '.js',
    'python': '.py',
    'java': '.java',
    'c': '.c',
    'cpp': '.cpp',
    'c++': '.cpp',
    'c#': '.cs',
    'ruby': '.rb',
    'php': '.php',
    'swift': '.swift',
    'objective-c': '.m',
    'kotlin': '.kt',
    'typescript': '.ts',
    'go': '.go',
    'perl': '.pl',
    'rust': '.rs',
    'scala': '.scala',
    'haskell': '.hs',
    'lua': '.lua',
    'shell': '.sh',
    'sql': '.sql',
    'html': '.html',
    'css': '.css'
    # Add more file extensions here, make sure the key is the same as the language prop in CodeBlock.tsx component
}

def generate_random_string(length: int, lowercase: bool = False) -> str:
    """
    Generates a random string of the specified length.

    Args:
        length (int): The length of the random string to generate.
        lowercase (bool, optional): Whether to convert the generated string to lowercase. Defaults to False.

    Returns:
        str: The generated random string.

    """
    chars = 'ABCDEFGHJKLMNPQRSTUVWXY3456789'  # Excluding similar-looking characters like Z, 2, I, 1, O, 0
    result = ''
    for _ in range(length):
        result += random.choice(chars)
    return result.lower() if lowercase else result
