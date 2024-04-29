<<<<<<< HEAD
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
=======
import os
from flask import Flask, jsonify
>>>>>>> e520f8ce0fdba7ef347b38f7ae11640865eb6dff
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)  # Permite solicitações de qualquer origem

<<<<<<< HEAD
# Rota principal
@app.route('/api/pergunta')
def get_question():
    # Obter o número da questão da query string, ou 0 se não estiver presente
    question_number = int(request.args.get('numero', 1))

=======
# Função para realizar o scraping
def scrape_question(question_number):
>>>>>>> e520f8ce0fdba7ef347b38f7ae11640865eb6dff
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
            correct_answer_element = soup.find(class_="answer correct")
            correct_answer = correct_answer_element.get_text(strip=True) if correct_answer_element else "Nenhuma resposta correta encontrada."
        else:
            # Se nenhum elemento com a classe 'answers' for encontrado, definir uma mensagem de resposta padrão
            answer_texts = ["Nenhum elemento com a classe 'answers' encontrado."]
            correct_answer = "Nenhuma resposta correta encontrada."
        # URL da imagem
        image_url = f"https://www.bomcondutor.pt/assets/images/questions/{question_number}.jpg"
<<<<<<< HEAD

        # Renderizar o template HTML com os dados da pergunta
        return render_template('template.html', question_text=question_text, answer_texts=answer_texts, correct_answer=correct_answer, image_url=image_url, question_number=question_number)
    else:
        # Se ocorrer um erro ao acessar a página, retornar um erro HTTP 500
        return jsonify({"error": "Erro ao acessar a página"}), 500
=======
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
>>>>>>> e520f8ce0fdba7ef347b38f7ae11640865eb6dff

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
