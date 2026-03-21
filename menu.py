import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Button:
    """Button class with enhanced hover effects"""
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 28, bold=True)
        
    def update(self, pos):
        """Update hover state"""
        self.is_hovered = self.rect.collidepoint(pos)
        
    def draw(self, surface):
        """Draw button with hover effect"""
        # Color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color
        
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        
        border_color = (255, 255, 255) if self.is_hovered else (200, 200, 200)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=10)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, pos):
        """Check if button was clicked"""
        return self.rect.collidepoint(pos)


class Menu:
    """Main Menu class"""
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        
        self.bg_color = (30, 30, 40) 
        self.accent_color = (100, 200, 255)
        self.accent_dark = (50, 150, 200)
        self.button_color = (50, 100, 150)
        self.button_hover = (100, 150, 200)
        self.text_color = (255, 255, 255)
        
        self.font_title = pygame.font.SysFont('Arial', 80, bold=True)
        self.font_subtitle = pygame.font.SysFont('Arial', 32, italic=True)
        self.font_small = pygame.font.SysFont('Arial', 20)
        
        button_width = 250
        button_height = 60
        button_x = 100
        button_y_start = 250
        button_gap = 100
        
        self.start_button = Button(
            button_x, button_y_start, 
            button_width, button_height, 
            "START", self.button_color, self.button_hover, self.text_color
        )
        
        self.instructions_button = Button(
            button_x, button_y_start + button_gap,
            button_width, button_height,
            "INSTRUCTIONS", self.button_color, self.button_hover, self.text_color
        )
        
        self.settings_button = Button(
            button_x, button_y_start + button_gap * 2,
            button_width, button_height,
            "SETTINGS", self.button_color, self.button_hover, self.text_color
        )
        
        self.quit_button = Button(
            button_x, button_y_start + button_gap * 3,
            button_width, button_height,
            "QUIT", self.button_color, self.button_hover, self.text_color
        )
        
        self.buttons = [
            self.start_button,
            self.instructions_button,
            self.settings_button,
            self.quit_button
        ]
        
        # State
        self.current_screen = 'main' 
        self.selected_level = 0

    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update(pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            if self.current_screen == 'main':
                if self.start_button.is_clicked(pos):
                    self.current_screen = 'level_select'
                elif self.instructions_button.is_clicked(pos):
                    self.current_screen = 'instructions'
                elif self.settings_button.is_clicked(pos):
                    self.current_screen = 'settings'
                elif self.quit_button.is_clicked(pos):
                    return 'quit'
                    
            elif self.current_screen == 'level_select':
                return self.handle_level_select(pos)
                
            elif self.current_screen in ['instructions', 'settings']:
                self.current_screen = 'main'
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.current_screen != 'main':
                    self.current_screen = 'main'
                else:
                    return 'quit'
                    
        return None

    def handle_level_select(self, pos):
        """Handle level selection"""
        from settings import LEVEL_DATA
        
        num_levels = len(LEVEL_DATA)
        level_width = 100
        level_height = 100
        level_start_x = 400
        level_start_y = 250
        level_gap = 150
        
        for i in range(num_levels):
            x = level_start_x + (i % 3) * level_gap
            y = level_start_y + (i // 3) * level_gap
            rect = pygame.Rect(x, y, level_width, level_height)
            
            if rect.collidepoint(pos):
                return ('start_game', i)
        
        back_rect = pygame.Rect(50, 50, 100, 50)
        if back_rect.collidepoint(pos):
            self.current_screen = 'main'
            
        return None

    def draw_main_menu(self):
        """Draw main menu"""
        self.screen.fill(self.bg_color)
        
        right_x = SCREEN_WIDTH // 2
        
        pygame.draw.rect(
            self.screen, 
            self.accent_color, 
            (right_x, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT), 
            1, 3
        )
        
        game_title = self.font_title.render('GAME', True, self.accent_color)
        game_title_rect = game_title.get_rect(center=(right_x + SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
        self.screen.blit(game_title, game_title_rect)
        
        subtitle = self.font_subtitle.render('Adventure Quest', True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(right_x + SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        self.screen.blit(subtitle, subtitle_rect)
        
        for button in self.buttons:
            button.draw(self.screen)
        
        hint_text = self.font_small.render('ESC: Exit menu', True, (150, 150, 150))
        hint_rect = hint_text.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
        self.screen.blit(hint_text, hint_rect)

    def draw_level_select(self):
        """Draw level selection screen"""
        from settings import LEVEL_DATA
        
        self.screen.fill(self.bg_color)
        
        title = self.font_title.render('SELECT LEVEL', True, self.accent_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        back_button = Button(50, 50, 100, 50, 'BACK', 
                           self.button_color, self.button_hover, self.text_color)
        back_button.update(pygame.mouse.get_pos())
        back_button.draw(self.screen)
        
        num_levels = len(LEVEL_DATA)
        level_width = 100
        level_height = 100
        level_start_x = 400
        level_start_y = 250
        level_gap = 150
        
        for i in range(num_levels):
            x = level_start_x + (i % 3) * level_gap
            y = level_start_y + (i // 3) * level_gap
            
            rect = pygame.Rect(x, y, level_width, level_height)
            is_hovered = rect.collidepoint(pygame.mouse.get_pos())
            
            color = self.button_hover if is_hovered else self.button_color
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255) if is_hovered else (200, 200, 200), 
                           rect, 3, border_radius=10)
            
            level_num = self.font_title.render(str(i + 1), True, self.text_color)
            level_num_rect = level_num.get_rect(center=rect.center)
            self.screen.blit(level_num, level_num_rect)

    def draw_instructions(self):
        """Draw instructions screen"""
        self.screen.fill(self.bg_color)
        
        # Title
        title = self.font_title.render('INSTRUCTIONS', True, self.accent_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "LEFT / RIGHT : Move left and right",
            "X : Jump",
            "Z : Dash",
            "SPACE : Wall Grab",
            "R : Restart level",
            "",
            "Goal: Jump to the goal (G marker)",
            "Collect coins for points",
            "Avoid spikes and enemies",
        ]
        
        y = 150
        for instruction in instructions:
            if instruction == "":
                y += 30
                continue
            text = self.font_small.render(instruction, True, self.text_color)
            text_rect = text.get_rect(x=150, y=y)
            self.screen.blit(text, text_rect)
            y += 50
        
        hint = self.font_small.render('Click to go back to menu', True, (150, 150, 150))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)

    def draw_settings(self):
        """Draw settings screen"""
        self.screen.fill(self.bg_color)
        
        # Title
        title = self.font_title.render('SETTINGS', True, self.accent_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Settings options
        settings = [
            "Sound: On",
            "Difficulty: Normal",
            "Fullscreen: Off",
            "Game Speed: 60 FPS",
            "",
            "Coming Soon:",
            "  - Sound customization",
            "  - Difficulty settings",
            "  - Key bindings",
        ]
        
        y = 150
        for setting in settings:
            if setting == "":
                y += 30
                continue
            is_header = setting.startswith("Coming")
            font = self.font_subtitle if is_header else self.font_small
            text = font.render(setting, True, self.text_color)
            text_rect = text.get_rect(x=150, y=y)
            self.screen.blit(text, text_rect)
            y += 50
        
        hint = self.font_small.render('Click to go back to menu', True, (150, 150, 150))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)

    def draw(self):
        """Draw menu based on current state"""
        if self.current_screen == 'main':
            self.draw_main_menu()
        elif self.current_screen == 'level_select':
            self.draw_level_select()
        elif self.current_screen == 'instructions':
            self.draw_instructions()
        elif self.current_screen == 'settings':
            self.draw_settings()


class PauseMenu:
    """Pause Menu class for in-game pause"""
    def __init__(self):
        self.screen = pygame.display.get_surface()
        
        # Colors
        self.bg_color = (30, 30, 40)
        self.accent_color = (100, 200, 255)
        self.button_color = (50, 100, 150)
        self.button_hover = (100, 150, 200)
        self.text_color = (255, 255, 255)
        
        # Fonts
        self.font_title = pygame.font.SysFont('Arial', 60, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 20)
        
        button_width = 250
        button_height = 60
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y_start = 300
        button_gap = 100
        
        self.resume_button = Button(
            center_x, button_y_start,
            button_width, button_height,
            "RESUME", self.button_color, self.button_hover, self.text_color
        )
        
        self.main_menu_button = Button(
            center_x, button_y_start + button_gap,
            button_width, button_height,
            "MAIN MENU", self.button_color, self.button_hover, self.text_color
        )
        
        self.quit_button = Button(
            center_x, button_y_start + button_gap * 2,
            button_width, button_height,
            "QUIT", self.button_color, self.button_hover, self.text_color
        )
        
        self.buttons = [self.resume_button, self.main_menu_button, self.quit_button]
    
    def handle_event(self, event):
        """Handle pause menu events"""
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update(pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            if self.resume_button.is_clicked(pos):
                return 'resume'
            elif self.main_menu_button.is_clicked(pos):
                return 'main_menu'
            elif self.quit_button.is_clicked(pos):
                return 'quit'
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'resume'
        
        return None
    
    def draw(self):
        """Draw pause menu with semi-transparent overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_title.render('PAUSED', True, self.accent_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(self.screen)
        
        hint = self.font_small.render('Press ESC to resume', True, (150, 150, 150))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)
