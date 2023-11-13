import client_settings
from operator_tcp_adapter import OperatorTCPadaptor_Client
import pygame

# Initialize Pygame
pygame.init()

# Setting up the clock and FPS
clock = pygame.time.Clock()
client_fps = 60

def run_client():
    print("Running Tank wars Operator client. Connecting to " + client_settings.serverIp + ":" + str(client_settings.serverPort))
    print("Using Tank operator: " + str(type(client_settings.tankoperator)) + " (Change this in client_settings.py if needed)")
    print("Press Ctrl-C or close the window to quit client")

    try:
        op = OperatorTCPadaptor_Client(client_settings.serverIp, client_settings.serverPort, client_settings.tankoperator)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    print("g")

            while op.run_client():
                pass

            clock.tick(client_fps)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        pygame.quit()

if __name__ == "__main__":
    run_client()
    print("Quitting Client")
