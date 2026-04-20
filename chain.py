import pygame

class ChainNode:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.old_pos = pygame.math.Vector2(pos)
        self.radius = 4

    def update(self, gravity, obstacles, dt_factor):
        vel = (self.pos - self.old_pos) * 0.98
        self.old_pos = pygame.math.Vector2(self.pos)
        self.pos += vel + pygame.math.Vector2(0, gravity * dt_factor)
        self.constrain_to_obstacles(obstacles)

    def constrain_to_obstacles(self, obstacles):
        node_rect = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)
        for sprite in obstacles:
            if sprite.rect.colliderect(node_rect):
                d_left = node_rect.right - sprite.rect.left
                d_right = sprite.rect.right - node_rect.left
                d_top = node_rect.bottom - sprite.rect.top
                d_bottom = sprite.rect.bottom - node_rect.top
                
                m = min(d_left, d_right, d_top, d_bottom)
                if m == d_top: self.pos.y = sprite.rect.top - self.radius
                elif m == d_bottom: self.pos.y = sprite.rect.bottom + self.radius
                elif m == d_left: self.pos.x = sprite.rect.left - self.radius
                elif m == d_right: self.pos.x = sprite.rect.right + self.radius
                self.old_pos = pygame.math.Vector2(self.pos)

class Chain:
    def __init__(self, num_nodes, max_length):
        self.num_nodes = num_nodes
        self.max_length = max_length
        self.node_dist = max_length / num_nodes
        self.nodes = [ChainNode((0, 0)) for _ in range(num_nodes)]
        self.sub_steps = 5

    def update(self, p1_center, p2_center, obstacles, player):
        sub_gravity = 0.6 / self.sub_steps
        sub_pull = 0.35 / self.sub_steps
        dt_f = 1.0 / self.sub_steps

        for _ in range(self.sub_steps):
            self.nodes[0].pos = pygame.math.Vector2(p1_center)
            self.nodes[-1].pos = pygame.math.Vector2(p2_center)

            for i in range(1, self.num_nodes - 1):
                self.nodes[i].update(sub_gravity, obstacles, dt_f)

            for _ in range(5):
                for i in range(self.num_nodes - 1):
                    n1, n2 = self.nodes[i], self.nodes[i+1]
                    diff = n1.pos - n2.pos
                    dist = diff.length()
                    if dist > 0:
                        err = (dist - self.node_dist) / dist
                        push = diff * err * 0.5
                        if i != 0: n1.pos -= push
                        if i != self.num_nodes - 2: n2.pos += push
                
                for i in range(1, self.num_nodes - 1):
                    self.nodes[i].constrain_to_obstacles(obstacles)

        curr_dist = p1_center.distance_to(p2_center)
        if curr_dist > self.max_length:
            pull_dir = (p2_center - p1_center).normalize()
            pull_mag = (curr_dist - self.max_length) * 0.35
            self.move_with_collision(player, pull_dir * pull_mag, obstacles)

    def move_with_collision(self, player, delta, obstacles):
        player.rect.x += int(delta.x)
        for s in obstacles:
            if s.rect.colliderect(player.rect):
                if delta.x > 0: player.rect.right = s.rect.left
                elif delta.x < 0: player.rect.left = s.rect.right
        
        player.rect.y += int(delta.y)
        for s in obstacles:
            if s.rect.colliderect(player.rect):
                if delta.y > 0: 
                    player.rect.bottom = s.rect.top
                    player.on_ground = True
                    player.m.direction.y = 0
                elif delta.y < 0: 
                    player.rect.top = s.rect.bottom
                    player.m.direction.y = 0
        player.remainder_x = player.remainder_y = 0

    def draw(self, surface, offset, p1_center, p2_center):
        dist = p1_center.distance_to(p2_center)
        color = (120, 120, 120) if dist < self.max_length * 0.85 else (255, 60, 60)
        for i in range(self.num_nodes - 1):
            pygame.draw.line(surface, color, self.nodes[i].pos - offset, self.nodes[i+1].pos - offset, 3)
        for i in range(self.num_nodes):
            if 0 < i < self.num_nodes - 1:
                pygame.draw.circle(surface, (60, 60, 60), self.nodes[i].pos - offset, 3)