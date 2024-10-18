from utils import get_random_element, url_verificator, number_verificator, clean_text
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import json
import re

def connext_button(browser):
    """Conecta com o proxy do TOR pelo botão connect button"""
    attempts = 0
    while attempts <= 3:
        try:
            connect_button = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.ID, "connectButton"))
            )
            if connect_button:
                connect_button.click()
                break
            else:
                print("Não foi possível encontrar o botão de conectar")
        except Exception as e:
            print({"Error in connect button": f"{e}"})
        finally:
            attempts += 1
            
def scrape_duckduckgo(browser, query):
    """Executa uma pesquisa no DuckDuckGo e retorna o conteúdo da página."""
    search_url = f"https://duckduckgo.com/?q={query}"
    try:
        input_area = WebDriverWait(browser, 6).until(
            EC.visibility_of_element_located((By.ID, "search-input"))
        )
    except Exception as e:
        print({"Error in input area 1": f"{e}"})
    
    browser.get(search_url)
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "search_form_input"))
    )
    return BeautifulSoup(browser.page_source, "html.parser")

def scrape_duckduckgo_search_first_input(browser, query):
    """Executa uma pesquisa no DuckDuckGo e retorna o conteúdo da página."""
    search_url = f"https://duckduckgo.com/?q={query}"
    try:
        input_search_area = WebDriverWait(browser, 6).until(
            EC.visibility_of_element_located((By.ID, "search_form_input"))
        )
    except Exception as e:
        print({"Error in search input": f"{e}"})
    
    browser.get(search_url)
    return BeautifulSoup(browser.page_source, "html.parser")


def extract_links_from_search(content, regex_url):
    """Extrai os links válidos da pesquisa DuckDuckGo."""
    sites = content.find_all("a", attrs={"class": "eVNpHGjtxRBq_gLOfGDr LQNqh2U1kzYxREs65IJu"})
    return [site['href'] for site in sites if url_verificator(site['href'], regex_url)]

def scrape_question_page(link, agents_list, regex_number, question_number):
    """Realiza o scraping de uma página de questão e retorna as informações."""
    user_agent = get_random_element(agents_list)
    headers = {"User-Agent": user_agent}
    response = requests.get(link, headers=headers)
    content_page = BeautifulSoup(response.text, "html.parser")
    
    question_section = content_page.find("div", attrs={"class": "sec-spacer pt-50"})
    if not question_section:
        return None
    
    header = question_section.find("div", attrs={"class": "question-discussion-header"})
    if not header or number_verificator(header.text, regex_number) != question_number:
        return None

    question_body = question_section.find("div", attrs={"class": "question-body mt-3 pt-3 border-top"})
    discussion_body = question_section.find("div", attrs={"class": "discussion-container"})
    most_voteted_question = extract_most_voted_question(question_body)
    question_text = extract_question_text(question_body)
    alternatives = extract_alternatives(question_body)
    discussion = extract_discussion(discussion_body)

    return {
        "question_number": question_number,
        "link": link,
        "question_text": question_text,
        "alternatives": alternatives,
        "most_voted_question": most_voteted_question,
        "discussion": discussion
    }

def extract_question_text(question_body):
    """Extrai o texto da pergunta e verifica se há uma imagem."""
    questionary = question_body.find("p", attrs={"class": "card-text"})
    if not questionary:
        return ""
    
    text = questionary.text
    img_question = questionary.find("img", attrs={"class": "in-exam-image"})
    if img_question:
        text += f"\n[IMAGE: https://examtopics.com{img_question['src']} FIM]\n"
    return text

def extract_alternatives(question_body):
    """Extrai as alternativas de múltipla escolha."""
    alternatives = question_body.find_all("li", attrs={"class": "multi-choice-item"})
    return [alt.text for alt in alternatives]

def extract_discussion(discussion_body):
    """Extrai a discussão da questão e estrutura em formato hierárquico."""
    def extract_comments(comment_element):
        comments = []
        if comment_element:
            for comment in comment_element.find_all('div', class_='media comment-container', recursive=False):
                comment_text = comment.find('div', attrs={"class": "comment-content"}).get_text(strip=True)
                reply_section = comment.find('div', class_='comment-replies')
                comment_text = clean_text(comment_text)
                comment_data = {
                    'comment': comment_text,
                    'replies': extract_comments(reply_section) if reply_section else []
                }
                comments.append(comment_data)
        return comments

    if discussion_body:
        return extract_comments(discussion_body)
    return []

def extract_most_voted_question(question_body):
    """Extrai a/as alternativa mais votada."""
    most_votate = question_body.find("div", attrs={"class": "voted-answers-tally d-none"})
    json_most_votate = most_votate.find("script", attrs={"type": "application/json"}).text
    data = json.loads(json_most_votate)
    list_voted = []
    for item in data:
        if item["is_most_voted"]:
            list_voted.append({"Mais votada": item["voted_answers"], "Total de votos": item["vote_count"]})
    return list_voted

def extract_question_image(regex, content):
    """Extrai a imagem da questão."""
    match = re.search(regex, content)
    if match != None:
        return match.group(1)
    else:
        return None
    
def exclude_image_question(regex, content):
    """Remove a imagem da questão do texto."""
    return re.sub(regex, "", content)