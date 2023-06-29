import re
from typing import List, Optional
from tiktoken import Tiktoken
from readability import Document
from similarity import calc_cosine_similarity, create_embedding

def extract_text_from_html(html: str) -> str:
    """
    Extracts text content from HTML using Readability.

    Args:
        html (str): The HTML content.

    Returns:
        str: The extracted text content.
    """
    doc = Document(html)
    parsed = doc.summary()
    return clean_source_text(parsed)

def get_token_size(text: str, encoding: Tiktoken) -> int:
    """
    Calculates the token size of the given text using Tiktoken encoding.

    Args:
        text (str): The text to calculate the token size for.
        encoding (Tiktoken): The Tiktoken encoding.

    Returns:
        int: The token size of the text.
    """
    tokens = encoding.encode(text)
    return len(tokens)

def slice_by_token_size(encoding: Tiktoken, text: str, start: int, end: int) -> str:
    """
    Slices the given text based on the specified start and end token indices.

    Args:
        encoding (Tiktoken): The Tiktoken encoding.
        text (str): The text to slice.
        start (int): The start token index.
        end (int): The end token index.

    Returns:
        str: The sliced text.
    """
    tokens = encoding.encode(text)
    sliced_tokens = tokens[start:end]
    decoded = encoding.decode(sliced_tokens)
    return decoded.decode()

def chunk_text_by_token_size(encoding: Tiktoken, text: str, chunk_token_size: int) -> List[str]:
    """
    Splits the text into chunks based on the specified token size.

    Args:
        encoding (Tiktoken): The Tiktoken encoding.
        text (str): The text to split into chunks.
        chunk_token_size (int): The size of each chunk in terms of tokens.

    Returns:
        List[str]: The list of text chunks.
    """
    tokens = encoding.encode(text)
    chunks = [tokens[i:i+chunk_token_size] for i in range(0, len(tokens), chunk_token_size)]
    decoded_chunks = [encoding.decode(chunk).decode() for chunk in chunks]
    return decoded_chunks

async def get_similar_chunks(encoding: Tiktoken, input: str, text: str, chunk_size: int, api_key: Optional[str] = None) -> List[str]:
    """
    Retrieves similar text chunks from the given input text.

    Args:
        encoding (Tiktoken): The Tiktoken encoding.
        input (str): The input text to find similar chunks for.
        text (str): The target text to search for similar chunks.
        chunk_size (int): The size of each chunk in terms of tokens.
        api_key (str, optional): The API key for creating embeddings. Defaults to None.

    Returns:
        List[str]: The list of similar text chunks, sorted by similarity score.
    """
    input_embedding = await create_embedding(input, api_key)
    chunks = chunk_text_by_token_size(encoding, text, chunk_size)
    chunk_embeddings = []
    for chunk in chunks:
        embedding = await create_embedding(chunk, api_key)
        chunk_embeddings.append({
            'embedding': embedding,
            'chunk': chunk
        })
    chunk_similarities = []
    for chunk_embedding in chunk_embeddings:
        similarity = calc_cosine_similarity(input_embedding, chunk_embedding['embedding'])
        chunk_similarities.append({
            'similarity': similarity,
            **chunk_embedding
        })
    sorted_chunks = sorted(chunk_similarities, key=lambda c: c['similarity'], reverse=True)
    return [c['chunk'] for c in sorted_chunks]

def clean_source_text(text: str) -> str:
    """
    Cleans the source text by removing extra whitespaces, tabs, and newlines.

    Args:
        text (str): The source text to clean.

    Returns:
        str: The cleaned text.
    """
    cleaned = re.sub(r"(\n){4,}", "\n\n\n", text.strip())
    cleaned = re.sub(r"\n\n", " ", cleaned)
    cleaned = re.sub(r" {3,}", "  ", cleaned)
    cleaned = re.sub(r"\t", "", cleaned)
    cleaned = re.sub(r"\n+(\s*\n)*", "\n", cleaned)
    return cleaned

def extract_url(text: str) -> Optional[str]:
    """
    Extracts the first URL found in the given text.

    Args:
        text (str): The text to search for URLs.

    Returns:
        Optional[str]: The extracted URL or None if no URL is found.
    """
    regex = r"(?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+(?::\d+)?(?:\/\S*)?"
    urls = re.findall(regex, text)
    return urls[0] if urls else None

