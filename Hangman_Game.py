import random
import re
import pygame
import math


pygame.init()

screen = pygame.display.set_mode((1000,600))
running = True
is_playing = False
is_changing_menu = False

playBackground = pygame.image.load("img/background_play_button.jpg")
playBackground = pygame.transform.scale(playBackground, (1000,600))

hangmanBackgroung = pygame.image.load("img/background_hangman_game.jpeg")
hangmanBackgroung = pygame.transform.scale(hangmanBackgroung,(1000,600))

font = pygame.font.Font(None, 70)
letter_font = pygame.font.SysFont("Inkfree",35)

button = pygame.image.load("img/play_button.png")
button = pygame.transform.scale(button,(200,200))
button_rect = button.get_rect(center=(hangmanBackgroung.get_width()/2,hangmanBackgroung.get_height()/2))

continu_button = pygame.image.load("img/continu_button.png")
continu_button = pygame.transform.scale(continu_button,(300,200))
continu_button_rect = continu_button.get_rect(center=(hangmanBackgroung.get_width()/2,550))

text = font.render("Play", True, "white")
text_rect = text.get_rect(center=(button.get_width()/2, button.get_height()/2))

game_pres ="Ce jeu est un pendu sauf que au lieu de finir pendu vous avez simplement des points de pénalité \nEssayez de gagner avec le moins de points de pénalité possible :)\nEt je précise que vous n'avez pas d'autre choix que de jouer à ce jeu :)"
game_pres_font = pygame.font.SysFont("Inkfree",50)

surface = pygame.Surface((200,200))

alphabet = []
startx = 200
starty = 450
gap = 10
radius = 25




fichier = open("dictionary.txt")
WORDS = fichier.read().split("\n")
playerPenality : int = 0
morethancpt = ""
guestWordorLetter : str

def drawalphabet() :
    for l in alphabet :
        if l['visible'] == True :
            letter_surface = letter_font.render(l["letter"],True,'purple')
            screen.blit(letter_surface,(l["x"] - letter_surface.get_width()/2,l["y"] - letter_surface.get_height()/2))

def placeWords(letter : str) :
    showfindword = ""
    for l in range(len(findThisWorld)) :
        if (findThisWorld[l] in  letter) :
            showfindword = showfindword + findThisWorld[l]
        else:
            showfindword = showfindword + "_"
    return showfindword
def display_text(surface, text, pos, font, color) :
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words,True,color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= 800:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height

def display_word(surface,word,pos,font,color) :
    showWord = ""
    for letter in word :
        showWord = showWord+letter
    word_surface = font.render(showWord,True,color)
    surface.blit(word_surface,pos)

def display_word_with_space(surface,word,pos,font,color) :
    showWord = ""
    for letter in word :
        showWord = showWord+letter+" "
    word_surface = font.render(showWord,True,color)
    surface.blit(word_surface,pos)



while (running == True) :

    for event in pygame.event.get() :
        if (event.type == pygame.QUIT) :
            running = False
            pygame.quit()
        elif (event.type == pygame.MOUSEBUTTONDOWN) :
            if (button_rect.collidepoint(pygame.mouse.get_pos())) :
                    is_changing_menu = True


            if (continu_button_rect.collidepoint(pygame.mouse.get_pos()) and is_playing == False) :
                for index in range(26):
                    alphabet.append({"x": (startx + (2 * radius + gap) * (index % 13)),
                                     "y": starty + (2 * radius + gap) * (index // 13), "letter": chr(ord('A') + index),
                                     'visible': True})
                is_playing = True
                findThisWorld: str = random.choice(WORDS)
                playerPenality = 0
                letters: str = ""
                aiword = findThisWorld
                aiadvice = random.choice(aiword)
                occurenceLetter = {}
                winner: bool = False;
                cpt: int;
                morethancpt = ""
                for i in findThisWorld:
                    cpt = 0
                    if (i in morethancpt):
                        pass
                    else:
                        for j in findThisWorld:
                            if (j == i):
                                cpt = cpt + 1
                        if (cpt > 1):
                            morethancpt = morethancpt + i
                        occurenceLetter[i] = cpt
                strpenality = str(playerPenality)
            m_x, m_y = pygame.mouse.get_pos()
            for letter in alphabet :
                               x = letter["x"]
                               y = letter["y"]
                               dis = math.sqrt( (x - m_x)**2 + (y - m_y)**2)
                               if(dis < radius) :
                                   letter['visible'] = False
                                   if(aiword != '') :
                                    aiadvice = random.choice(aiword)

                                   if (len(aiword) <= 4) :
                                       aiadvice = findThisWorld

                                   guestWordorLetter = letter["letter"]
                                   if (guestWordorLetter.lower() in findThisWorld):
                                       aiword = aiword.replace(guestWordorLetter.lower(), "")
                                       if (guestWordorLetter in letters):
                                           playerPenality = playerPenality + 3
                                           print(f"Vous avez {playerPenality} point de penalités")
                                       else:
                                           playerPenality = playerPenality + 1
                                           letters = letters + guestWordorLetter.lower()
                                           aiword = aiword.replace(guestWordorLetter.lower(), "")
                                       if (placeWords(letters) == findThisWorld):
                                           winner = True
                                           is_playing = False
                                           best_score_file = open("best_score.txt")
                                           best_score = best_score_file.read()
                                       else:
                                           print(f"\n {placeWords(letters)} \n")
                                           print(f"{guestWordorLetter} : {occurenceLetter[guestWordorLetter.lower()]}")
                                           print(f"Vous avez {playerPenality} points de pénalité")
                                   else:
                                       playerPenality = playerPenality + 3
                                       print(f"\n {placeWords(letters)} \n")
                                       print(f"\n"
                                             f"Vous avez {playerPenality} point de penalités")

    if (is_changing_menu == True):
        screen.blit(hangmanBackgroung, (0, 0))
        if (is_playing == True):

            text = f"Vous avez {playerPenality} point de penalités"
            display_word_with_space(screen, placeWords(letters), (300, 100), game_pres_font, "blue")
            display_word(screen, text, (470, 50), game_pres_font, 'blue')
            display_word(screen,f"Try '{aiadvice}'",(600,100),letter_font, 'blue')
            drawalphabet()
        else:
            display_text(screen, game_pres, (250, 20), game_pres_font, 'purple')
            screen.blit(continu_button, continu_button_rect)
    else:
        screen.blit(playBackground, (0, 0))
        screen.blit(button, button_rect)
        button.blit(text, text_rect)


    pygame.display.update()



def case_insensitive_search_and_replace(file_path, search_word, replace_word):
   with open(file_path, 'r') as file:
      file_contents = file.read()

      pattern = re.compile(re.escape(search_word), re.IGNORECASE)
      updated_contents = pattern.sub(replace_word, file_contents)

   with open(file_path, 'w') as file:
      file.write(updated_contents)




def winnerMessage() :
   print(f"Oui bon t'as juste eu de la chance croit pas t'es fort :-@ \n"
         f"T'as gagné avec {playerPenality} point de pénalités"
         f"Le mot était {findThisWorld}")


def game() :
    while (winner == False):
        tryFullword: str = ""
        guestWordorLetter: str = ""
        while (tryFullword.lower() != "yess" and tryFullword.lower() != "no"):
            if (len(aiword) < 4):
                display_text(hangmanBackgroung, placeWords(letters), (0, 0), game_pres_font, 'purple')
                display_text(hangmanBackgroung, findThisWorld, (0, 50), game_pres_font, 'purple')
            else:
                display_text(hangmanBackgroung, placeWords(letters), (0, 0), game_pres_font, 'purple')
                display_text(hangmanBackgroung, random.choice(aiword), (0, 50), game_pres_font, 'purple')
            tryFullword = input(
                "Voulez vous tentez un mot en entier ? (écrivez 'yess' pour dire oui ou 'no' dire non) : ")

        if (tryFullword == "yess"):
            while (len(guestWordorLetter) < 2 or guestWordorLetter == ""):
                guestWordorLetter = input("Entre un mot et oublie pas qu'un mot c'est pas une lettre : ")

            if (guestWordorLetter == findThisWorld):
                winner = True
                best_score_file = open("best_score.txt")
                best_score = best_score_file.read()
                if (playerPenality < int(best_score)):
                    case_insensitive_search_and_replace("best_score.txt", best_score, str(playerPenality))
                    display_text(hangmanBackgroung, f"T'as eu le meilleur score : {playerPenality}", (0, 100), "purple")
                else:
                    print(f"Le meilleure score est {best_score} et ton score à toi est {playerPenality}")
                winnerMessage()
            else:
                playerPenality = playerPenality + 5
                print(f"Vous avez {playerPenality} points de pénalité")
        else:
            while (len(guestWordorLetter) > 1 or guestWordorLetter == ""):
                guestWordorLetter = input("Entre une lettre chacal : ")
            if (guestWordorLetter in findThisWorld):
                if (guestWordorLetter in letters):
                    playerPenality = playerPenality + 3
                    print(f"Vous avez {playerPenality} point de penalités")
                else:
                    aiword = aiword.replace(guestWordorLetter, "")
                    playerPenality = playerPenality + 1
                    letters = letters + guestWordorLetter
                if (placeWords(letters) == findThisWorld):
                    winner = True
                    best_score_file = open("best_score.txt")
                    best_score = best_score_file.read()
                    if (playerPenality < int(best_score)):
                        case_insensitive_search_and_replace("best_score.txt", best_score, str(playerPenality))
                        print(f"T'as eu le meilleur score : {playerPenality}")
                    else:
                        print(f"Le meilleure score est {best_score} et ton score à toi est {playerPenality}")
                    winnerMessage()
                else:
                    print(f"\n {placeWords(letters)} \n")
                    print(f"{guestWordorLetter} : {occurenceLetter[guestWordorLetter]}")
                    print(f"Vous avez {playerPenality} points de pénalité")
            else:
                playerPenality = playerPenality + 3
                print(f"\n {placeWords(letters)} \n")
                print(f"\n"
                      f"Vous avez {playerPenality} point de penalités")



#print(WORDS)

print("\n"
      "Ce jeu est un pendu sauf que au lieu de finir pendu vous avez simplement des points de pénalité \n"
      "\n"
      "Le mot a trouver est l'un des mots de la liste ci- dessus"
      "\n"
      "Essayez de gagner avec le moins de points de pénalité possible :)"
      "\n"
      "Et je précise que vous n'avez pas d'autre choix que de jouer à ce jeu :)"
      "\n")






























































