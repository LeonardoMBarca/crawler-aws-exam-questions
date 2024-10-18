def question_formater(infos):
    """Formata apenas as informações das questões em um dicionário"""
    return {
        'question_number': infos.get('question_number', ''),
        'link': infos.get('link', ''),
        'question_text': infos.get('question_text', ''),
        'alternatives': infos.get('alternatives', [])
    }

def discussion_formater(infos):
    """Formata apenas as informações da discussão em um dicionário"""
    return {
        'question_number': infos.get('question_number', ''),
        'link': infos.get('link', ''),
        'discussion': infos.get('discussion', []),
        'most_voted_question': infos.get('most_voted_question', [])
    }