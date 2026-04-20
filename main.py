import pygame, sys
from settings import *
from level import Level
from menu import Menu, PauseMenu
import network

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('GameDev_3')
        self.clock = pygame.time.Clock()
        
        self.bgm = None  # Initialize first
        self.import_assets()
        
        self.network = network.Network()
        self.menu = Menu()
        self.pause_menu = PauseMenu()
        
        self.current_level_index = 0
        self.level = None
        self.status = 'menu' 

    def import_assets(self):
        def get_surf(path, fallback_color):
            try:
                return pygame.image.load(path).convert_alpha()
            except Exception as e:
                print(f"[ERROR] Cannot load img at {path}: {e}")
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(fallback_color)
                return surf

        self.surfaces = {
            'player_default': get_surf('Assets/graphics/Default.png', PLAYER_COLOR),
            'player_jump': get_surf('Assets/graphics/Jump.png', 'blue'),
            'player_die': get_surf('Assets/graphics/Die.png', 'red'),
            'player_dash':    get_surf('Assets/graphics/Dash.png', 'purple'),
            'tile': get_surf('Assets/graphics/Brick.png', 'grey'),
            'bg_tile': get_surf('Assets/graphics/bg_tile.png', (50, 50, 50)),
            'brick':get_surf('Assets/graphics/Brick.png', 'brown'),
            'coin': get_surf('Assets/graphics/Coin.png', 'yellow'),
            'star': get_surf('Assets/graphics/Star.png', 'gold'),
            'enemy': get_surf('Assets/graphics/Signus.png', 'red'),
            'Enemy01': get_surf('Assets/graphics/Enemy01.png', 'white'),
            'spike': get_surf('Assets/graphics/Spike.png', 'purple'),
            'bounce': get_surf('Assets/graphics/Bounce.png', 'orange'),
            'goal': get_surf('Assets/graphics/goal.png', 'green'),
            'key': get_surf('Assets/graphics/key.png', 'cyan'),
            'door': get_surf('Assets/graphics/key_hole.png', 'brown'),
            'Item01': get_surf('Assets/graphics/Item01.png', 'green'),
            'Item02': get_surf('Assets/graphics/Item02.png', 'pink'),
            'q_normal': get_surf('Assets/graphics/Normal.png', 'yellow'),
            'q_popped': get_surf('Assets/graphics/Popped.png', (100, 100, 100)),
        }
        
        # Load BGM
        try:
            pygame.mixer.music.load('Assets/super-mario-bros-theme-song.mp3')
            self.bgm = True
            print("[INFO] BGM loaded successfully!")
            # Set volume to maximum
            pygame.mixer.music.set_volume(1.0)
            print(f"[INFO] BGM Volume set to: {pygame.mixer.music.get_volume()}")
        except Exception as e:
            print(f"[WARNING] Cannot load BGM: {e}")
            self.bgm = False

    def next_level(self):
        if self.bgm:
            pygame.mixer.music.stop()
        self.current_level_index += 1
        if self.current_level_index < len(LEVEL_DATA):
            self.level = Level(LEVEL_DATA[self.current_level_index], self.surfaces, self.next_level, self.menu.key_bindings)
            self.start_level()
        else:
            self.status = 'menu'
            self.current_level_index = 0

    def restart_current_level(self):
        if self.bgm:
            pygame.mixer.music.stop()
        self.start_level()
        if self.bgm and self.menu.sound_enabled:
            pygame.mixer.music.play(-1)  # Restart BGM

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.status == 'menu':
                    result = self.menu.handle_event(event)
                    if result == 'quit':
                        pygame.quit()
                        sys.exit()
                    elif isinstance(result, tuple):
                        if result[0] == 'start_game':
                            self.current_level_index = result[1]
                            self.start_level()
                            self.status = 'playing'
                        elif result[0] == 'connect_lobby':
                            if self.network.connect(result[1]):
                                self.menu.lobby_connected = True
                                self.menu.is_host = (self.network.id == 1)
                                # Gửi thông tin màu của mình ngay khi vừa kết nối
                                self.network.send({"type": "lobby_color", "color_idx": self.menu.current_color_idx})
                        elif result[0] == 'update_color':
                            self.network.send({"type": "lobby_color", "color_idx": result[1]})
                        elif result[0] == 'update_lobby_level':
                            self.network.send({"type": "lobby_level", "level": result[1]})
                        elif result[0] == 'start_multiplayer':
                            self.network.send({"type": "host_start", "level": result[1]})
                            self.current_level_index = result[1]
                            self.start_level()
                            self.status = 'playing'
                    elif result == 'disconnect_lobby':
                        self.network.connected = False
                        self.menu.lobby_connected = False

                elif self.status == 'playing':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r: self.restart_current_level()
                        if event.key == pygame.K_p:
                            self.status = 'paused'
                            if self.bgm: pygame.mixer.music.pause()
                        if event.key == pygame.K_ESCAPE:
                            self.status = 'menu'
                            self.menu.current_screen = 'main'
                            if self.bgm: pygame.mixer.music.stop()
                
                elif self.status == 'paused':
                    result = self.pause_menu.handle_event(event)
                    if result == 'resume':
                        self.status = 'playing'
                        if self.bgm and self.menu.sound_enabled: pygame.mixer.music.unpause()
                    elif result == 'main_menu':
                        self.status = 'menu'
                        self.menu.current_screen = 'main'
                        if self.bgm: pygame.mixer.music.stop()
                    elif result == 'quit':
                        pygame.quit(); sys.exit()

            # --- LOGIC ĐỒNG BỘ MẠNG TRONG MENU ---
            if self.status == 'menu':
                if self.menu.lobby_connected:
                    net_events = self.network.get_events()
                    for ne in net_events:
                        if ne.get('type') == 'lobby_color':
                            self.menu.remote_color_idx = ne.get('color_idx')
                            # Gửi lại thông tin của mình để người kia thấy mình
                            self.network.send({"type": "lobby_sync", "remote_color": self.menu.current_color_idx, "level": self.menu.multiplayer_selected_level})
                        elif ne.get('type') == 'lobby_sync':
                            self.menu.remote_color_idx = ne.get('remote_color')
                            self.menu.multiplayer_selected_level = ne.get('level')
                        elif ne.get('type') == 'lobby_level':
                            self.menu.multiplayer_selected_level = ne.get('level')
                        elif ne.get('type') == 'host_start':
                            self.current_level_index = ne.get('level')
                            self.start_level()
                            self.status = 'playing'
                self.menu.draw()
            
            elif self.status == 'playing':
                self.screen.fill(BG_COLOR)
                if self.menu.is_multiplayer and self.network.connected:
                    events = self.network.get_events()
                    sync_events = []
                    for e in events:
                        if e.get('type') == 'state':
                            if getattr(self.level, 'remote_player', None):
                                self.level.remote_player.update_network_state(e)
                        else:
                            sync_events.append(e)
                    self.level.process_network_events(sync_events)
                    
                    if getattr(self.level, 'player', None):
                        p = self.level.player
                        self.network.send({
                            "type": "state", "x": p.rect.x, "y": p.rect.y,
                            "facing_right": p.facing_right, "is_dead": p.is_dead,
                            "is_big": p.is_big, "is_dashing": p.m.is_dashing
                        })
                        
                    if getattr(self.level, 'outbound_events', None):
                        for ev in self.level.outbound_events:
                            self.network.send(ev)
                        self.level.outbound_events.clear()

                self.level.run()
                self.draw_pause_button()
            
            elif self.status == 'paused':
                self.screen.fill(BG_COLOR)
                self.level.run()
                self.pause_menu.draw()

            pygame.display.update()
            self.clock.tick(self.menu.game_speed)
    
    def draw_pause_button(self):
        """Draw pause button during gameplay"""
        font = pygame.font.SysFont('Arial', 24, bold=True)
        pause_text = font.render('P: PAUSE', True, (255, 255, 255))
        pause_rect = pause_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        
        bg_rect = pause_rect.inflate(20, 20)
        pygame.draw.rect(self.screen, (50, 100, 150), bg_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 150, 200), bg_rect, 2, border_radius=8)
        
        self.screen.blit(pause_text, pause_rect)

    
    def start_level(self):
        """Start a specific level"""
        player_color = self.menu.player_color_options[self.menu.current_color_idx] if self.menu.is_multiplayer else None
        remote_color_idx = (self.menu.current_color_idx + 1) % len(self.menu.player_color_options)
        remote_color = self.menu.player_color_options[remote_color_idx] if self.menu.is_multiplayer else None
        
        self.level = Level(LEVEL_DATA[self.current_level_index], self.surfaces, self.next_level, self.menu.key_bindings, self.menu.is_multiplayer, player_color, remote_color)
        
        # Play BGM (check if sound is enabled in menu settings)
        print(f"[DEBUG] Start level - BGM loaded: {self.bgm}, Sound enabled: {self.menu.sound_enabled}")
        if self.bgm and self.menu.sound_enabled:
            pygame.mixer.music.play(-1)  # -1 means loop infinitely
            print(f"[DEBUG] Now playing BGM... volume={pygame.mixer.music.get_volume()}")

if __name__ == '__main__':
    game = Game()
    game.run()