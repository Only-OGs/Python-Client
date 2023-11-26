import game.globals
import pygame
import pygame_gui

pygame.init()

#init Music
main_music = pygame.mixer.music.load(filename="assets/Music/StartMenuMusic.mp3")
pygame.mixer.music.play(loops=5,fade_ms=40,start=0)
pygame.mixer.music.set_volume(0.01)

#Register input Fenster
manager_register = pygame_gui.UIManager((game.globals.screen_width, game.globals.screen_height))
register_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 350), (360, 60)),
                                           manager=manager_register, object_id="#name", placeholder_text="Name")

register_passwort = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 450), (360, 60)),
                                               manager=manager_register, object_id="#passwort",
                                               placeholder_text="Passwort", visible=str)

#Login input Fenster
manager_Login = pygame_gui.UIManager((game.globals.screen_width, game.globals.screen_height))
login_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 350), (360, 60)),
                                                 manager=manager_Login, object_id="#name", placeholder_text="Name")

login_passwort = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 450), (360, 60)),
                                                     manager=manager_Login, object_id="#passwort",
                                                     placeholder_text="Passwort", visible=str)
#Option felder
manager_option = pygame_gui.UIManager((game.globals.screen_width, game.globals.screen_height))
#Music
music_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((game.globals.screen_width//2 - (game.globals.slider_width//2), game.globals.screen_height - 100),
                                                     (game.globals.slider_width, game.globals.slider_height)),start_value=0.01, value_range=((0.00) ,(0.10)), manager=manager_option
                                                      )