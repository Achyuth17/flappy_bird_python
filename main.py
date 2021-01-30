import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 600))
    screen.blit(floor_surface, (floor_x_pos + 576, 600))


def create_pipe():
    pipe_pos_y = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(588, pipe_pos_y))
    top_pipe = pipe_surface.get_rect(midbottom=(588, pipe_pos_y - 185))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 7
    new_pipes = [pipe for pipe in pipes if pipe.right > -40]
    return new_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 600:
        death_sound.play()
        can_score = True
        return False

    return True


def rotate_bird(bird):
    return pygame.transform.rotate(bird, -1.35 * bird_pos_y)


def bird_animation():
    new_bird_surface = bird_frames[bird_index]
    new_bird_rect = new_bird_surface.get_rect(center=(100, bird_rect.centery))
    return new_bird_surface, new_bird_rect


def score_display(game_state):
    if game_state == "game":
        score_surface = game_font.render(str(int(score)), True, (155, 255, 100))
        score_rect = score_surface.get_rect(center=(288, 85))
        screen.blit(score_surface, score_rect)

    if game_state == "game_over":
        score_surface = game_font.render("Current Score : " + str(int(score)), True, (195, 155, 100))
        score_rect = score_surface.get_rect(center=(288, 85))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render("High Score : " + str(int(high_score)), True, (255, 255, 100))
        high_score_rect = high_score_surface.get_rect(center=(288, 545))
        screen.blit(high_score_surface, high_score_rect)


def update_high_score(score, high_score):
    if score > high_score:
        high_score = score

    return high_score


def pipe_score_check():
    global score
    global can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                point_sound.play()
                score += 1
                can_score = False

            if pipe.centerx <= 150 and can_score and bird_rect.colliderect(pipe):
                if score:
                    score -= 1

            if pipe.centerx < 70:
                can_score = True


# pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 700))  # create a screen (576 - width ,1024 - height)
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 45)

# Game variables
gravity = 0.25
bird_pos_y = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load("assets/background-day.png").convert_alpha()
bg_surface = pygame.transform.scale(bg_surface, (576, 700))

floor_surface = pygame.image.load("assets/base.png").convert_alpha()
floor_surface = pygame.transform.scale(floor_surface, (576, 112))
floor_x_pos = 0

bird_downflap = pygame.transform.scale(pygame.image.load("assets/bluebird-downflap.png").convert_alpha(), (50, 40))
bird_midflap = pygame.transform.scale(pygame.image.load("assets/bluebird-midflap.png").convert_alpha(), (50, 40))
bird_upflap = pygame.transform.scale(pygame.image.load("assets/bluebird-upflap.png").convert_alpha(), (50, 40))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 350))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface, (50, 40))
# bird_rect = bird_surface.get_rect(center=(100, 350))

pipe_surface = pygame.image.load("assets/pipe-green.png").convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (70, 400))
pipe_list = []
pipe_height = [300, 375, 450, 525]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_over_surface = pygame.transform.scale(pygame.image.load("assets/message.png").convert_alpha(), (270, 230))
game_over_rect = game_over_surface.get_rect(center=(288, 300))

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
point_sound = pygame.mixer.Sound("sound/sfx_point.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")

while True:
    # draw all our elements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_pos_y = 0
                bird_pos_y -= 7
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 350)
                bird_pos_y = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_pos_y += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_pos_y
        screen.blit(rotated_bird, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)

        # Score
        pipe_score_check()
        score_display("game")

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_high_score(score, high_score)
        score_display("game_over")

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(80)  # 60 times this while loops runs in 1 sec
