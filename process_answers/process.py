from bs4 import BeautifulSoup
import csv

def to_csv():
    with open('process_answers/answers.html', encoding='utf-8') as qa:
        soup = BeautifulSoup(qa, 'html.parser')
        questions = [x.text.strip() for x in soup.find_all('span', {'class': 'q'})]
        answers = [x.text.strip() for x in soup.find_all('span', {'class': 'a'})]

    with open('qa.csv', 'w' , encoding='utf-8', newline='') as qa:
        writer = csv.writer(qa)
        # writer.writerow(['questions', 'answers'])
        for i in range(len(answers)):
            writer.writerow([questions[i], answers[i]])