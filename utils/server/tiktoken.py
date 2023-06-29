import os
import json
import tiktoken

initialized = False

def get_tiktoken_encoding(model):
    """
    Retrieves the Tiktoken encoding for the specified model.

    Args:
        model (str): The model for which to retrieve the Tiktoken encoding.

    Returns:
        Tiktoken: The Tiktoken encoding for the specified model.

    Raises:
        FileNotFoundError: If the required Tiktoken data file is not found.
    """
    global initialized

    if not initialized:
        wasm_binary = open('./public/tiktoken_bg.wasm', 'rb').read()
        tiktoken.init(lambda: wasm_binary)
    initialized = True

    if 'text-davinci-' in model:
        p50k_data = json.load(open('./path/to/p50k_base.json'))
        return tiktoken.Tiktoken(p50k_data['bpe_ranks'], p50k_data['special_tokens'], p50k_data['pat_str'])
    if 'gpt-3.5' in model or 'gpt-4' in model:
        return tiktoken.encoding_for_model(model, {
            '': 100264,
            '': 100265,
            '': 100266,
        })
    cl100k_data = json.load(open('./path/to/cl100k_base.json'))
    return tiktoken.Tiktoken(cl100k_data['bpe_ranks'], cl100k_data['special_tokens'], cl100k_data['pat_str'])
