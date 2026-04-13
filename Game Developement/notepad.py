import pygame
import sys

pygame.init()

# Screen setup
W, H = 600, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Notepad")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Colors
color_inactive = pygame.Color('gray')
color_active = pygame.Color('dodgerblue')
color = color_inactive

# Input box
input_box = pygame.Rect(10, 10, 580, 480)

active = False
running = True

# Use lines instead of single text
lines = [""]

def save_note(content):
    with open("note.txt","w") as f:
        f.write(content)
    print("The Note saved succesfully")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_note(str(lines).strip())
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
                color = color_active
            else:
                active = False
                color = color_inactive

        if event.type == pygame.KEYDOWN and active:

            # ENTER → new line
            if event.key == pygame.K_RETURN:
                lines.append("")

            # BACKSPACE
            elif event.key == pygame.K_BACKSPACE:
                if lines[-1]:
                    lines[-1] = lines[-1][:-1]
                else:
                    if len(lines) > 1:
                        lines.pop()

            # NORMAL TEXT
            else:
                char = event.unicode
                current_line = lines[-1] + char

                # 🔥 Check width before adding
                if font.size(current_line)[0] >= input_box.width - 20:
                    lines.append(char)   # move to next line
                else:
                    lines[-1] = current_line

    # DRAW
    screen.fill((33, 33, 33))

    # Render all lines
    y = 15
    for line in lines:
        text_surface = font.render(line, True, "white")
        screen.blit(text_surface, (15, y))
        y += 30

    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()
    clock.tick(60)