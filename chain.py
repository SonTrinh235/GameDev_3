import pygame

class ChainNode:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.old_pos = pygame.math.Vector2(pos)

    def update(self, gravity, obstacles):
        vel = (self.pos - self.old_pos) * 0.95
        self.old_pos = pygame.math.Vector2(self.pos)
        self.pos += vel + pygame.math.Vector2(0, gravity)

        for sprite in obstacles:
            if sprite.rect.collidepoint(self.pos):
                if vel.y > 0: 
                    self.pos.y = sprite.rect.top - 1
                    self.old_pos.y = self.pos.y
                elif vel.y < 0:
                    self.pos.y = sprite.rect.bottom + 1
                    self.old_pos.y = self.pos.y

class Chain:
    def __init__(self, num_nodes, max_length):
        self.num_nodes = num_nodes
        self.max_length = max_length
        self.node_dist = max_length / num_nodes
        self.nodes = [ChainNode((0, 0)) for _ in range(num_nodes)]

    def update(self, p1_center, p2_center, obstacles, player):
        self.nodes[0].pos = pygame.math.Vector2(p1_center)
        self.nodes[-1].pos = pygame.math.Vector2(p2_center)

        for i in range(1, self.num_nodes - 1):
            self.nodes[i].update(0.6, obstacles)

        for _ in range(15):
            for i in range(self.num_nodes - 1):
                n1, n2 = self.nodes[i], self.nodes[i+1]
                diff = n1.pos - n2.pos
                dist = diff.length()
                if dist > 0:
                    error = (dist - self.node_dist) / dist
                    push = diff * error * 0.5
                    if i != 0: n1.pos -= push
                    if i != self.num_nodes - 2: n2.pos += push

        curr_dist = p1_center.distance_to(p2_center)
        if curr_dist > self.max_length:
            pull_dir = (p2_center - p1_center).normalize()
            pull_magnitude = (curr_dist - self.max_length) * 0.25
            
            self.move_with_collision(player, pull_dir * pull_magnitude, obstacles)

    def move_with_collision(self, player, delta, obstacles):
        player.rect.x += int(delta.x)
        for sprite in obstacles:
            if sprite.rect.colliderect(player.rect):
                if delta.x > 0: player.rect.right = sprite.rect.left
                elif delta.x < 0: player.rect.left = sprite.rect.right
        
        player.rect.y += int(delta.y)
        for sprite in obstacles:
            if sprite.rect.colliderect(player.rect):
                if delta.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
                    player.m.direction.y = 0
                elif delta.y < 0: 
                    player.rect.top = sprite.rect.bottom
                    player.m.direction.y = 0
        
        player.remainder_x = player.remainder_y = 0

    def draw(self, surface, offset, p1_center, p2_center):
        dist = p1_center.distance_to(p2_center)
        color = (120, 120, 120) if dist < self.max_length * 0.85 else (255, 60, 60)
        
        for i in range(self.num_nodes - 1):
            start = self.nodes[i].pos - offset
            end = self.nodes[i+1].pos - offset
            pygame.draw.line(surface, color, start, end, 3)
            
        for i in range(self.num_nodes):
            if 0 < i < self.num_nodes - 1:
                pygame.draw.circle(surface, (60, 60, 60), self.nodes[i].pos - offset, 3)