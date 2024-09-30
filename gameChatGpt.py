import json
import random
import openai
from keywords import KEYWORDS_JSON

# OpenAI API 키 설정 
openai.api_key = 'chatGpt_API_KEY'

# JSON 문자열을 파이썬 객체로 변환
def parse_keywords_json(json_str):
    data = json.loads(json_str)
    keywords = [word['keyword'] for entry in data for word in entry['words']]
    return keywords

# 키워드 로드
def load_keywords():
    return parse_keywords_json(KEYWORDS_JSON)

# 데이터 로드
keywords = load_keywords()

# OpenAI ChatGPT 3.5 Turbo 호출
def get_model_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI playing the '20 Questions' game."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error generating response."

# 질문 프롬포트(모델에 역활전달)
def generate_question_prompt(previous_questions):
    return (
        f"You are an AI playing the '20 Questions' game. Your goal is to ask yes/no questions to guess the keyword.\n"
        f"Category is country or city or landmark.\n"
        f"First, identify the category. After identifying the category, narrow down the possibilities by asking about the region (e.g., 'Is it a country in Asia?').\n"
        f"Here are the previous questions and answers:\n"
        f"{previous_questions}\n"
        f"Do not repeat any of the previous questions. Ask a new yes/no question that will help narrow down the possibilities.\n\n"
        f"New question:"
    )

# 대답 프롬포트(모델에 역활전달)
def generate_answer_prompt(question, keyword):
    return (
        f"The secret keyword is: '{keyword}'. Based on this, answer the question: '{question}' with 'yes' or 'no'.\nAnswer:"
    )

# 추측(정답) 프롬포트(모델에 역활전달)
def final_guess_prompt(previous_questions):
    return (
        f"You have asked the following questions:\n"
        f"{previous_questions}\n\n"
        f"Based on these questions and answers, make a final guess about what the keyword might be.\n"
        f"Final guess:"
    )

# 20 Questions 게임을 진행하는 함수
def play_20_questions(keyword):
    print("Let's play 20 Questions!")
    print(f"Think of something related to a {keyword}.")

    num_questions = 0
    max_questions = 20
    previous_questions = []

    while num_questions < max_questions:
        num_questions += 1
        
        # 질문 생성
        prompt = generate_question_prompt(' '.join(previous_questions))
        question = get_model_response(prompt)
        
        # 질문 출력
        print(f"Question {num_questions}: {question}")
        
        # 자동으로 대답 생성
        answer = get_model_response(generate_answer_prompt(question, keyword))
        
        # 대답 출력
        print(f"Answer: {answer}")

        # 이전 질문에 추가
        previous_questions.append(f"Q: {question} A: {answer}")

        # 10번째 질문 이후에 정답을 맞추는 흐름
        if num_questions == 10:
            print(f"Is it related to {keyword}?")
            if answer.lower() == 'yes':
                print(f"Awesome! I guessed it in {num_questions} questions!")
                return
            else:
                print("Let me keep trying...")

    # 최종 추측
    final_guess = get_model_response(final_guess_prompt(' '.join(previous_questions)))
    
    # 최종 추측과 실제 키워드 출력
    print(f"Final guess: {final_guess}")
    print(f"The actual keyword was: {keyword}")
    print(f"Sorry, I couldn't guess within {max_questions} questions.")

# 게임 시작
def start_game():
    print("Starting 20 Questions Game with ChatGPT 3.5-turbo and local data...")

    if len(keywords) == 0:
        print("No keywords found in the keywords data.")
        return

    # 랜덤 키워드 선택
    selected_keyword = random.choice(keywords)
    play_20_questions(selected_keyword)

# 게임 시작
start_game()
