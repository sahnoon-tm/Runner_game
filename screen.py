from typing import Any
import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 400))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 400:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400

    def animation_status(self):
        if self.rect.bottom < 400:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_status()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 310
        else:
            snail_1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 400

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1100, 1200), y_pos))

    def animation_status(self):
        self.animation_index += 0.1
        if self.animation_index >= 2:
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_status()
        self.rect.x -= 6
        self.distroy()

    def distroy(self):
        if self.rect.x <= -100:
            self.kill()


# impletmenting time


def display_score():

    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f"Score : {current_time} ", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(500, 70))
    screen.blit(score_surface, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_index, player_surface
    if player_rect.bottom < 400:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Runner")

# Create a clock object to control the game's frame rate
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/font.ttf", 50)
bg_music = pygame.mixer.Sound("audio/bg_music.mp3")
bg_music.set_volume(0.1)
bg_music.play(loops=-1)
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Load images and scale them to fit the screen
sky_surface = pygame.image.load("graphics/sky.png").convert()
sky_surface_fit = pygame.transform.scale(sky_surface, (1000, 400))
ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_surface_fit = pygame.transform.scale(ground_surface, (1000, 100))

# obstacles
snail_frame_1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
fly_frame_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]
obstacle_list = []

# Create a rectangle for the player surface for positioning
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(100, 400))

# indro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(500, 250))
player_gravity = 0
start_time = 0
score = 0

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(500, 110))
game_message = test_font.render("Press space to run ", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(500, 400))

game_active = False

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 200)

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 400:
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 400:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    # Draw the background and other surfaces
    if game_active:

        screen.blit(sky_surface_fit, (0, 0))
        screen.blit(ground_surface_fit, (0, 400))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collition
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_list.clear()
        player_rect.midbottom = (100, 400)
        player_gravity = 0

        score_message = test_font.render(
            f"Your score: {score} ", False, (111, 196, 169)
        )
        score_message_rect = score_message.get_rect(center=(500, 400))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
