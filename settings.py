import pygame

# Screen
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1200
TILE_SIZE = 32
FPS = 60

# Colors
BG_COLOR = '#060b14'
PLAYER_COLOR = '#ff4d4d'

# Physics
GRAVITY = 0.4
PLAYER_SPEED = 4.5
JUMP_SPEED = -12
TERMINAL_VELOCITY = 12

# Dash
DASH_SPEED = 14
DASH_DURATION = 250
DASH_COOLDOWN = 500

# Wall / Grab
WALL_SLIDE_SPEED = 2
WALL_FRICTION = 0.5

# Key Mapping
K_DASH = pygame.K_z
K_JUMP = pygame.K_x
K_GRAB = pygame.K_SPACE

LEVEL_0 = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXGGGGGGGX',
    '                                                                          XXXXX                                                                      X',
    '                                                                          XXXXX                                                                      X',
    '                                                          S               XXXXX                                                                      X',
    '                                                                          XXXXX                                                                      X',
    '                                                                          XXXXX                                                       XXXX           X',
    '                                                                                                                                      XXXX           X',
    '                                                                                                                                      XXX            X',
    '                                                                                                                                      XXX            X',
    '                                XXXXXXXXX                                                    XXXXXXXX                            XXXXXXXX            X',
    '                                XXXXXXXXX                                                    XXXXXXXX                                   X            X',
    '                                XXXXXXXXX                                                        XXXX            X                                   X',
    '                                XXXXXXXXX                                                        XXXX            XXXX                                X',
    '                XXXXXXX         XXXXXXXXX            C                                             XX            XXXX                                X',
    'P               XXXXXXX         XXXXXXXXX          XXXXX                 ^^^^^^                     X            XXXX          ^^^^^          S      X',
    'XXXXXXXXX       XXXXXXX         XXXXXXXXX^^^^^^^               J         XXXXXX                                    XX          XXXXX                 X',
    'XXXXXXXXX       XXXXXXX         XXXXXXXXXXXXXXXX^^^^^^^       XXX        XXXXX                                                 XXXXX                 X',
    'XXXXXXXXX       XXXXXXX^^^^^^^^^XXXXXXXXXXXXXXXXXXXXXXX       XXX         XXXX                                          ^^^^^^^XXXXX^^^^^^^^^^^^^^^^^X',
    'XXXXXXXXX^^^^^^^XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX^^^^^^^^XXXXXXXXX                                      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                              XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_1 = [
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                           E                                                                                                          ',
    '                                          XXXX                                                                                                        ',
    '                                          XXXX                                                                                                        ',
    '                                          XXXX                                         XXXX                                                           ',
    '                              C           XXXX                                         XXXX                                                           ',
    '                             XXXX         XXXX                                         XXXX                                                           ',
    '                             XXXX         XXXX                            XXXX         XXXX                                                           ',
    '                             XXXX         XXXX                            XXXX         XXXX                                                           ',
    '                             XXXX         XXXX                            XXXX         XXXX                               C                           ',
    '                             XXXX         XXXX             C              XXXX         XXXX                             XXXXX                         ',
    '                             XXXX         XXXX           XXXXX            XXXX         XXXX                                                           ',
    '                             XXXX         XXXX                            XXXX         XXXX                                            G              ',
    '                             XXXX         XXXX                            XXXX         XXXX                                          XXXXX            ',
    'P            C               XXXX         XXXX                            XXXX         XXXX              E                                            ',
    'XXXXX      XXXXX             XXXX         XXXX                            XXXX         XXXX           XXXXXXX                                         ',
    'XXXXX                        XXXX         XXXX                            XXXX         XXXX           XXXXXXX                                         ',
    'XXXXX    S       S           XXXX    S    XXXX             S              XXXX    S    XXXX      S    XXXXXXX       S        S                        ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_2 = [
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                              C                       ',
    '                                               C                        C                                                   XXXXX                     ',
    '                                             XXXXX                    XXXXX                                                                           ',
    '                                                                                                    C                                                 ',
    '                                                                                                  XXXXX                                               ',
    '                   C                                                                                                                        G         ',
    'P                XXXXX                                                                                                                    XXXXX       ',
    'XXXXX                           XXXXX                 XXXXX                        XXXXX                     XXXXX                                    ',
    'XXXXX                           XXXXX                 XXXXX                        XXXXX                     XXXXX                                    ',
    'XXXXX      S             S      XXXXX      S          XXXXX           S            XXXXX          S          XXXXX             S                      ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_3 = [
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                             XXXX                                                     ',
    '                                                                                             XXXX                                                     ',
    '                                                                                             XXXX                                                     ',
    '                                              XXXX                                           XXXX                                                     ',
    '                                              XXXX                                           XXXX                                                     ',
    '                                              XXXX                                           XXXX                                                     ',
    '                             XXXX             XXXX                                           XXXX                               C                     ',
    '                             XXXX             XXXX                                           XXXX                             XXXXX                   ',
    '                             XXXX             XXXX            C                              XXXX                                                     ',
    '                             XXXX             XXXX          XXXXX                            XXXX                                           G         ',
    'P            C               XXXX             XXXX                         E                 XXXX                 E                           XXXXX       ',
    'XXXXX      XXXXX             XXXX             XXXX                      XXXXXXX              XXXX              XXXXXXX                                ',
    'XXXXX                        XXXX      S      XXXX                      XXXXXXX              XXXX              XXXXXXX                                ',
    'XXXXX    S       S           XXXX   XXXXXXX   XXXX   S         S        XXXXXXX       S      XXXX       S      XXXXXXX       S        S               ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_4 = [
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                                                                                      ',
    '                                                                                             XXXX                                                     ',
    '                                                                                             XXXX                                                     ',
    '                                                                                             XXXX                                                     ',
    '                                                                                             XXXX                                                     ',
    '                                              XXXX                                           XXXX                                                     ',
    '                                              XXXX                                           XXXX                                                     ',
    '                             XXXX             XXXX                                           XXXX                               C                     ',
    '                             XXXX             XXXX                                           XXXX                             XXXXX                   ',
    '                             XXXX             XXXX            C                              XXXX                                                     ',
    '                                                            XXXXX                            XXXX                                           G         ',
    'P            C               XXXX                                          E                 XXXX                 E                           XXXXX       ',
    'XXXXX      XXXXX             XXXX             XXXX                      XXXXXXX              XXXX              XXXXXXX                                ',
    'XXXXX                        XXXX      S      XXXX                      XXXXXXX              XXXX              XXXXXXX                                ',
    'XXXXX    S       S           XXXX   XXXXXXX   XXXX   S         S        XXXXXXX       S      XXXX       S      XXXXXXX       S        S               ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_DATA = [LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4]