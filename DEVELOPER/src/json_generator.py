import json

def generate_json_question(data, output_filename):
    """Gera um arquivo JSON contendo questões e alternativas."""
    questions_data = []

    for item in data:
        question_info = {
            "question_number": item['question_number'],
            "link": item['link'],
            "question_text": item['question_text'],
            "alternatives": item['alternatives']
        }
        questions_data.append(question_info)

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(questions_data, f, ensure_ascii=False, indent=4)
    
    print(f"JSON '{output_filename}' gerado com sucesso!")

def generate_json_discussion(data, output_filename):
    """Gera um arquivo JSON contendo discussões, link e alternativas mais votadas."""
    discussions_data = []

    for item in data:
        discussion_info = {
            "question_number": item['question_number'],
            "link": item['link'],
            "most_voted_question": item['most_voted_question'],
            "discussion": item['discussion']
        }
        discussions_data.append(discussion_info)

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(discussions_data, f, ensure_ascii=False, indent=4)
    
    print(f"JSON '{output_filename}' gerado com sucesso!")


# file = ""
# with open(file, 'r', encoding='utf-8') as filee:
#     filee = json.load(filee)
# listr = [i for i in range(1, 357)]
# numbers = []
# for question in filee:
#     numbers.append(question['question_number'])
# print(list(set(listr) - set(numbers)))