import random
import re


def get_random_element(lst):
    """Retorna um elemento aleatório de uma lista."""
    return random.choice(lst)

def url_verificator(url, regex):
    """Verifica se a URL corresponde ao regex fornecido."""
    return bool(re.match(regex, url))

def number_verificator(content, regex_number):
    """Extrai o número da questão usando regex."""
    match = re.search(regex_number, content)
    return int(match.group(1)) if match else None

def clean_text(text):
    return text.replace("’", "'")
