from browser_setup import setup_browser
from scrapper import scrape_duckduckgo, scrape_duckduckgo_search_first_input, extract_links_from_search, scrape_question_page, connext_button
from formaters import question_formater, discussion_formater
from json_generator import generate_json_discussion, generate_json_question
from pdf_generator import convert_html_to_pdf
from html_generator import generate_html_for_questions, generate_html_for_discussions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

user_agents_file = r"/home/leonardo/Desktop/web_scrapping_aws_questions/user_agents/firefox/firefox_linux_agents.txt"
profile_path = r'C:\Users\leona\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\s2w7csgm.lionel_messi'
geckodriver_path = r'/home/leonardo/Desktop/web_scrapping_aws_questions/driver-tor/geckodriver.exe'
tor_browser_path = r'/home/leonardo/Desktop/tor-browser'

with open(user_agents_file, mode="r") as f:
    agents_list = f.read().splitlines()

regex_url = r"(https://www\.examtopics\.com/discussions/amazon/view/)(\d{2,8})(-exam-aws-certified-developer-associate-dva-c02-topic-1/)"
regex_number = r"Question\s#:\s(\d+)"
regex_image = r"\[IMAGE:\s(https://.*?)(\sFIM)]"

link_questoes = []
scraped_questions = []
scraped_discussions = []
success = 0
first_search = True

# Quantidade máxima de tentativas para cada questão
max_attempts = 5
browser = None
for i in range(450):
    attempts = 0  # Contador de tentativas para cada questão
    question_found = False  # Flag para determinar se a questão foi encontrada
    
    if i == 0:
        browser = setup_browser(profile_path, tor_browser_path, geckodriver_path)
        connext_button(browser)

    while attempts < max_attempts and not question_found:
        try:
            # Faz a consulta e tenta buscar o link da questão
            query = f"site:examtopics.com intitle:\"EXAM AWS CERTIFIED DEVELOPER - ASSOCIATE DVA-C02\" intitle:\"TOPIC 1 QUESTION {i+1} DISCUSSION\""
            
            if (attempts == 0 or attempts > 3) and first_search:
                content = scrape_duckduckgo(browser, query)
            else:
                content = scrape_duckduckgo_search_first_input(browser, query)
                
            links = extract_links_from_search(content, regex_url)

            for link in links:
                result = scrape_question_page(link, agents_list, regex_number, i+1)
                if result:
                    print(f"Link da questão {i+1} encontrado!")
                    link_questoes.append([i+1, link])

                    formatted_question = question_formater(result)
                    formatted_discussion = discussion_formater(result)

                    scraped_questions.append(formatted_question)
                    scraped_discussions.append(formatted_discussion)
                    
                    success += 1
                    question_found = True

                    if question_found:
                        first_search = False
                        break
                    
                else:
                    print(f"Questão {i+1} não encontrada ou não válida.")
                    

        except Exception as e:
            print(f"Erro ao buscar a questão {i+1}: {e}")
            if attempts >= 3:
                question_found = False  
        finally:
            if attempts >= 3:
                print(f"Erro persistente para a questão {i+1}. Reiniciando o navegador Tor...")
                browser.quit()
                browser = setup_browser(profile_path, tor_browser_path, geckodriver_path)
                connext_button(browser)
                first_search = True
# Resetar a flag para tentar a próxima questão

        attempts += 1  # Incrementa o número de tentativas
        if not question_found:
            print(f"Tentativa {attempts} falhou para a questão {i+1}. Retentando...")

    # Se após 4 tentativas a questão ainda não foi encontrada, pula para a próxima
    if not question_found:
        print(f"Falhou em encontrar a questão {i+1} após {max_attempts} tentativas. Pulando para a próxima questão.")
    time.sleep(1)
    
print(f"Quantidade de Sucesso: {success}")

# Salvamento dos links e resultados
link_questoes_df = pd.DataFrame(link_questoes, columns=["Questão", "Link"])
link_questoes_df.to_csv(r"C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\link\link_questoes.csv", index=False)

generate_json_question(scraped_questions, r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\processed\questions.json')
generate_json_discussion(scraped_discussions, r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\processed\discussions.json')

# Gerar HTML e PDF das questões e discussões
questions_file = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\processed\questions.json'
discussions_file = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\processed\discussions.json'
questions_output_file = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\html\questions.html'
discussions_output_file = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\html\discussions.html'

generate_html_for_questions(questions_file, questions_output_file, regex_image)
generate_html_for_discussions(discussions_file, discussions_output_file)

# Converter HTML para PDF
html_file_question = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\html\questions.html'
pdf_file_question = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\pdf\questions.pdf'
html_file_discussion = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\html\discussions.html'
pdf_file_discussion = r'C:\Users\leona\Desktop\web_scrapping_aws_questions\DEVELOPER\data\pdf\discussions.pdf'

convert_html_to_pdf(html_file_question, pdf_file_question)
convert_html_to_pdf(html_file_discussion, pdf_file_discussion)
