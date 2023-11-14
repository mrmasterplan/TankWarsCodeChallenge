import pygame

# colors
wheat = (245, 222, 179)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

red = (200, 0, 0)
light_red = (255, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)

color_lookup = {"red":red, "blue": blue, "green": green, "yellow": yellow}

s_font = pygame.font.SysFont("Arial", 25)
m_font = pygame.font.SysFont("Arial", 50)
l_font = pygame.font.SysFont("Arial", 85)
vs_font = pygame.font.SysFont("Arial", 18)

# defining function to get the fonts and sizes assigned with them by size names by default size="small"
def txt_object(txt, color, size="small"):
    if size == "small":
        txtSrfc = s_font.render(txt, True, color)
    if size == "medium":
        txtSrfc = m_font.render(txt, True, color)
    if size == "large":
        txtSrfc = l_font.render(txt, True, color)
    if size == "vsmall":
        txtSrfc = vs_font.render(txt, True, color)

    return txtSrfc, txtSrfc.get_rect()

# function for texts that has to appear over screen
def msg_screen_topleft(surface, message, color, topleft, size="small"):
    txtSrf, textRect = txt_object(message, color, size)
    textRect.topleft = topleft
    surface.blit(txtSrf, textRect)

def print_lines_on_surface(surface, lines, color):
    
    topleft = (50,50)

    def nextline(topleft):
        line_height = 60
        return (50, topleft[1] + line_height)
        
    for ll in lines:
        msg_screen_topleft(surface, ll, color, topleft)
        topleft = nextline(topleft)
    
def game_wait_for_players_screen(surface, clock, color_operator_dict):

    while True:
        surface.fill((0, 0, 0))
        start_pressed = False
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_s:
                    start_pressed = True

        line_height = 100
        topleft = (300,150)
        msg_screen_topleft(surface, "Waiting for players:", white, topleft, size="medium")
        ready_players = {}
        for color_key, operator in color_operator_dict.items():
            color = color_lookup[color_key]
            topleft = (300, topleft[1]+line_height)
            player_line = operator.get_operator_name()
            
            if player_line is None:
                player_line = "<Player not found>"
                try:
                    player_line = "<Waiting for player on:" + operator.get_connection_info_string() + ">"
                except:
                    pass
            else:
                ready_players[color_key] = operator

            msg_screen_topleft(surface, player_line, color, topleft, size="small")

        topleft = (300, topleft[1]+line_height)
        if len(ready_players) == len(color_operator_dict):
            msg_screen_topleft(surface, ">>> Ready! Press 's' to start! <<<", white, topleft, size="small")
        else:
            msg_screen_topleft(surface, "> Players NOT Ready! Press 's' to start anyway <", light_yellow, topleft, size="small")
        pygame.display.update()

        clock.tick(5) #fps

        if start_pressed:
            return ready_players
        