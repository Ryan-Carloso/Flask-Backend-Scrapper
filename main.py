import os
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Função para realizar o scraping
def scrape_question(question_number):
    # Construir a URL da página a ser scrapada com base no número da questão
    url = f"https://www.bomcondutor.pt/questao/{question_number}"
    # Enviar uma requisição GET para a página
    response = requests.get(url)
    # Verificar se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Parsear o conteúdo da página usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Encontrar o elemento com a classe 'question-text'
        question_text_element = soup.find(class_="question-text")
        question_text = question_text_element.get_text(strip=True) if question_text_element else "Nenhum elemento com a classe 'question-text' encontrado."
        # Encontrar o elemento com a classe 'answers'
        answers_element = soup.find(class_="answers")
        if answers_element:
            # Encontrar todos os elementos <li> dentro de answers_element
            list_items = answers_element.find_all("li")
            # Inicializar uma lista para armazenar os textos das respostas
            answer_texts = []
            # Iterar sobre cada elemento <li>
            for item in list_items:
                # Encontrar todos os elementos <span> dentro de cada <li>
                spans = item.find_all("span")
                # Inicializar uma lista temporária para armazenar os textos dos spans
                span_texts = []
                # Iterar sobre cada elemento <span> encontrado
                for span in spans:
                    # Extrair o texto do span e adicioná-lo à lista temporária
                    span_texts.append(span.get_text(strip=True))
                # Juntar os textos dos spans em uma string separada por vírgulas
                answer_text = ", ".join(span_texts)
                # Adicionar o texto da resposta à lista de textos das respostas
                answer_texts.append(answer_text)
            # Encontrar a resposta correta, se existir
            correct_answer_element = answers_element.find("li", class_="A correct")
            correct_answer = correct_answer_element.get_text(strip=True) if correct_answer_element else "Nenhuma resposta correta encontrada."
        else:
            # Se nenhum elemento com a classe 'answers' for encontrado, definir uma mensagem de resposta padrão
            answer_texts = ["Nenhum elemento com a classe 'answers' encontrado."]
            correct_answer = "Nenhuma resposta correta encontrada."
        # URL da imagem
        image_url = f"https://www.bomcondutor.pt/assets/images/questions/{question_number}.jpg"
        return {
            "question_text": question_text,
            "answer_texts": answer_texts,
            "correct_answer": correct_answer,
            "image_url": image_url,
            "question_number": question_number
        }
    else:
        return {"error": f"Erro ao acessar a página: {response.status_code}"}

# Rota para realizar o scraping e retornar os resultados em JSON
@app.route('/scrape')
def scrape():
    question_number = int(requests.args.get('numero', 1))
    scraped_data = scrape_question(question_number)
    return jsonify(scraped_data)

if __name__ == '__main__':
    # Usando a porta fornecida pelo Heroku ou, se não estiver disponível, a 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
