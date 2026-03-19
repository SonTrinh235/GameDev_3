import pygame

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 32
FPS = 60

# Colors
BG_COLOR = '#B8E1FF'
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

LEVEL_1 = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X                                                                                                                                                    X',
    'X                                                                                                                                                    X',
    'X                                                                           S                                                                        X',
    'X                                                                         XXXXX                                                                      X',
    'X                                                                         XXXXX                                                       XXXX           X',
    'X                                                                                                                                     XXXX           X',
    'X                                                                                                                                     XXX            X',
    'X                                   M                                                                                                 XXX     G      X',
    'X                               XXXXXXXXX                                                    XXXXXXXX                            XXXXXXXX            X',
    'X                               XXXXXXXXX                                                    XXXXXXXX                                   X            X',
    'X                               XXXXXXXXX                                                        XXXX            X                                   X',
    'X                  M            XXXXXXXXX                                                        XXXX            XXXX                                X',
    'X               XXXXXXX         XXXXXXXXX            C                                             XX            XXXX                                X',
    'X  P            XXXXXXX         XXXXXXXXX          XXXXX                 ^^^^^^                     X            XXXX          ^^^^^          S      X',
    'XFFXXFFFF                       XXXXXXXXX^^^^^^^               J         XXXXXX                                    XX          XXXXX                 X',
    'X                  C            XXXXXXXXXXXXXXXX^^^^^^^       XXX        XXXXX                                                 XXXXX                 X',
    'X               XXXXXXX^^^^^^^^^XXXXXXXXXXXXXXXXXXXXXXX       XXX         XXXX                                          ^^^^^^^XXXXX^^^^^^^^^^^^^^^^^X',
    'X^^^^^^^^^^^^^^^XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX^^^^^^^^XXXXXXXXX                                      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                              XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_0 = [
    'X                                                                                                                                                    X',
    'X                                                                                                                                                    X',
    'XX                                         S                                                                                                         X',
    'XXXX                                      FFFF                                                                                                       X',
    'XXXXXX                                    FFFF                                                                                                       X',
    'X                                                                                      XXXX                                                          X',
    'X P                           C                                                        XXXX                                                          X',
    'XFFFFFFFF                                                                              XXXX                                                          X',
    'XFFFFFFFF                                                                 XXXX         XXXX                                                          X',
    'XFFF                         FFFF                                         XXXX         XXXX                                                          X',
    'X                                           E                             XXXX         XXXX                               C                          X',
    'X                                       FFXXXXFF           C              XXXX         XXXX                             XXXXX                        X',
    'X                                         XXXX           FFFFF            XXXX         XXXX                                                          X',
    'X                                         XXXX                            XXXX         XXXX                                            G             X',
    'X                                         XXXX                            XXXX         XXXX                                          XXXXX           X',
    'X                                         XXXX                            XXXX         XXXX              E                                           X',
    'X^^^^      XXQXX       FFFFF              XXXX                            XXXX         XXXX           XXXXXXX                                        X',
    'XXXXX                                     XXXX                            XXXX         XXXX           XXXXXXX                                        X',
    'XXXX        1                             XXXX             S              XXXX    S    XXXX      S    XXXXXXX       S        S                       X',
    'XXXXXXXXXXXXXXXXXX                       XXXXXXFFFFFFFFFFFFFFFFFFFFFFFFFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
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
    'XXXXX    1       1      1      1XXXXX      S          XXXXX           S            XXXXX          S          XXXXX             S                      ',
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