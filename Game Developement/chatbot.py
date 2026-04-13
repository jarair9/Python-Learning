import pygame 
import sys
import openai
import os
from dotenv import load_dotenv

load_dotenv()
pygame.init()

def AIRESPONSE(text) -> str:
    "Creating AI to Response for User Query"
    client = openai.OpenAI(api_key=os.getenv("CEREBRAS_API_KEY"),base_url="https://api.cerebras.ai/v1")
    response = client.chat.completions.create(
    model="qwen-3-235b-a22b-instruct-2507",
    messages=[
        {"role": "user", "content": text,}
    ])
    result = response.choices[0].message.content
    return result

W = 800
H = 500
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Chatbot")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

input_box = pygame.Rect(50, 410, 700, 50)
color_inactive = pygame.Color('gray')
color_active = pygame.Color('dodgerblue')
color = color_inactive

text = ""
active = False
ai_response = ""  # Store AI response 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
                color = color_active
            else:
                active = False
                color = color_inactive

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    if text.strip():  # Only send if not empty
                        print("Entered:", text)
                        try: 
                            ai_response = AIRESPONSE(text)
                        except openai.APIConnectionError:
                            text = "Connection error try again"
                            print("Check Your connection")
                        text = ''  
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill((30, 30, 30))
    
    # Draw input box
    txt_surface = font.render(text, True, (255, 255, 255))

    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    
    # Draw AI response
    ai_text = font.render(ai_response, True, (100, 255, 100))
    screen.blit(ai_text, (20, 40))
    
    clock.tick(60)
    pygame.display.update()

pygame.quit()