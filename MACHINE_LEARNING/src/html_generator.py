import json
from bs4 import BeautifulSoup
from scrapper import extract_question_image, exclude_image_question

def generate_html_for_questions(questions_file, output_file, regex):
    with open(questions_file, 'r', encoding="utf-8") as f:
        questions = json.load(f)

    # Start HTML content for questions
    html_content = "<html><head><title>Questions</title></head><body>"

    # Add Questions
    for question in questions:
        html_content += f"<h1>Question {question['question_number']}</h1>"
        if (exclude_image_question(regex, question['question_text'])):
            html_content += f"<p><strong>Question:</strong> {exclude_image_question(regex, question['question_text'])}</p>"
        if (extract_question_image(regex, question['question_text'])):
            html_content += f"<img src='{extract_question_image(regex, question['question_text'])}'>"
        html_content += "<ul>"
        for alternative in question['alternatives']:
            html_content += f"<li>{alternative.strip()}</li>"
        html_content += "</ul>"
        html_content += f"<p><strong>Link:</strong> <a href='{question['link']}'>{question['link']}</a></p>"
        html_content += "<hr>"

    # End HTML content for questions
    html_content += "</body></html>"
    html_content = BeautifulSoup(html_content, 'html.parser').prettify()

    # Write HTML content to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_html_for_discussions(discussions_file, output_file):
    with open(discussions_file, 'r', encoding="utf-8") as f:
        discussions = json.load(f)

    # Start HTML content for discussions
    html_content = "<html><head><title>Discussions</title></head><body>"

    # Add Discussions
    for discussion in discussions:
        html_content += f"<h1>Discussion for Question {discussion['question_number']}</h1>"
        html_content += f"<p><strong>Link:</strong> <a href='{discussion['link']}'>{discussion['link']}</a></p>"
        html_content += "<h2>Most Voted</h2>"
        html_content += "<ul>"
        for vote in discussion['most_voted_question']:
            html_content += f"<li>{vote['Mais votada']}: {vote['Total de votos']} votes</li>"
        html_content += "</ul>"

        def add_comments(comments):
            content = ""
            for comment in comments:
                content += f"<div style='margin-left: 20px;'><p><strong>Comment:</strong> {comment['comment']}</p>"
                if comment['replies']:
                    content += "<h3>Replies:</h3><ul>"
                    content += add_comments(comment['replies'])
                    content += "</ul>"
                content += "</div>"
            return content

        html_content += "<h2>Discussion</h2>"
        html_content += "<div>"
        html_content += add_comments(discussion['discussion'])
        html_content += "</div>"

        html_content += "<hr>"

    # End HTML content for discussions
    html_content += "</body></html>"
    html_content = BeautifulSoup(html_content, 'html.parser').prettify()

    # Write HTML content to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)