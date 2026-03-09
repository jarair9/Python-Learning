import json
import os 
from mistralai import Mistral
import requests
import time
import ast
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# tngtech/deepseek-r1t-chimera:free
def typer(text, delay=0.04):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def parse_llm(text):
    text = text.strip()

    if not text:
        raise ValueError("LLM returned empty response")

    text = text.strip()

    
    if "```" in text:
        text = text.replace("```json", "")
        text = text.replace("```python", "")
        text = text.replace("```", "")

    text = text.strip()

    # Try JSON first if it works
    try:
        return json.loads(text)
    except Exception as e_json:
        pass

    # Try Python dict then try ast module
    try:
        return ast.literal_eval(text)
    except Exception as e_ast:
        print("\nFAILED TO PARSE LLM OUTPUT:")
        print(text)
        raise ValueError("LLM output not JSON or dict format")

def quix_gen_openrouter(lvl: str, topic: str, count: int):
    paths = "Projects\Jsons\data.json"
    client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"),base_url ="https://openrouter.ai/api/v1" )
    
    prompt = """Generate quiz. Output ONLY this format:
    {
        "1": {"question": "Q?", "options": ["A","B","C","D"], "answer": "correct", "explanation": "why"}
    }
    Rules:
    - Use string keys "1","2","3"
    - No markdown, no extra text
    - Match difficulty level
    - Include explanations"""
    
    response = client.chat.completions.create(
        model="z-ai/glm-4.5-air:free",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Create {count} questions on topic {topic} with difficulty level {lvl}."}
        ], 
        temperature=0.7
    )

    
    S =  response.choices[0].message.content
    
    clean = parse_llm(S)

    with open(paths, "w") as f:
        json.dump(clean, f)
    
 
def Quix_gen_mistral(lvl: str, topic: str, count: int):
    paths = "Projects\Jsons\database.json"
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    
    prompt = """Generate quiz. Output ONLY this format:
    {
    "1": {"question": "Q?", "options": ["A","B","C","D"], "answer": "correct", "explanation": "why"}
    }
    Rules:
    - Use string keys "1","2","3"
    - No markdown, no extra text
    - Match difficulty level
    - Include explanations"""
    
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Create {count} questions on topic {topic} with difficulty level {lvl}."}
        ], 
        temperature=0.7
        
    )

    
    S = response.choices[0].message.content
    
    clean = parse_llm(S)

    with open(paths, "w") as f:
        json.dump(clean, f)

    
    

def questioning_user():
    paths = "Projects\Jsons\database.json"
    correct = 0
    incorrect = 0
    
    with open(paths, "r") as f:
        data = json.load(f)
    
    for item in data.items():
        correct_answer = item[1]['answer']
        explanation = item[1]['explanation']
        question = item[1]['question']
        options_list = item[1]["options"]
        
        print()
        typer(f"Question {item[0]}: {question}")
        print()
        
        for option in options_list:  
            print(f"- {option}")
        
        answer = input("Enter Your Answer: ").strip().lower()
        
        if answer != correct_answer.lower(): 
            incorrect += 1
            typer("Incorrect Answer\n")
            print(f"Correct Answer: {correct_answer}")
            print(f"Explanation: {explanation}")  
        else:
            typer("Correct answer!\n")
            correct += 1
        
        print()
    
    print(f"You answered {correct} correctly out of {len(data)}")
    print(f"Your score: {(correct / len(data)) * 100:.1f}%")

def main():
    typer("Welcome to Our Quiz Competition\n")  
    print("-" * 30)
    
    topic = input("Enter Topic for Quiz: ")  
    level = input("Enter level of Questions (beginner, intermediate, advanced): ")  
    count = int(input("Enter how many questions you want to generate (integer): "))
    
    # Generate quiz with AI and save to file
    # Added Perameters
    quix_gen_openrouter(level, topic, count)
    
    
    # Start the quiz
    questioning_user()

if __name__ == "__main__":
    main()