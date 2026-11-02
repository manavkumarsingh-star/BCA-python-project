"""
PS No. 57: Car Racing Game
Course: Programming Fundamentals Using Python (RU-100-05-00058)
Program: BCA / First Semester / Section - 1A
University: Rungta International Skills University
Author: Manav Kumar Singh
Repository: https://github.com/manavkumarsingh-star/BCA-python-project

Problem Statement:
Create a 2D car racing game in which the player steers a car left and right on a road
using the arrow keys, avoids obstacle cars coming down from the top, and scores a point
for every obstacle passed. The game ends when the player's car collides with an obstacle.
"""

import os
import random
import sys
import pygame

# ---------------------------------------------------------------------------
# Game Constants (as specified in PS No. 57)
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60

ROAD_LEFT = 50
ROAD_RIGHT = 350
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT  # 300 px

CAR_WIDTH = 40
CAR_HEIGHT = 80

PLAYER_START_X = 180
PLAYER_START_Y = 500
PLAYER_STEP = 10  # Moves 10 px per key press

MIN_CAR_X = ROAD_LEFT               # 50 (left edge of road)
MAX_CAR_X = ROAD_RIGHT - CAR_WIDTH  # 310 (right edge of road: 310 + 40 = 350)

OBSTACLE_SPEED = 5
SPAWN_INTERVAL_FRAMES = 55

# Colors (RGB)
COLOR_GRASS = (34, 139, 34)
COLOR_ROAD = (60, 60, 65)
COLOR_BORDER = (240, 240, 240)
COLOR_LANE_LINE = (255, 215, 0)
COLOR_PLAYER = (30, 144, 255)
COLOR_PLAYER_ROOF = (180, 225, 255)
COLOR_OBSTACLE = (220, 50, 47)
COLOR_OBSTACLE_ROOF = (255, 190, 185)
COLOR_WHEEL = (20, 20, 20)
COLOR_TEXT = (255, 255, 255)
COLOR_OVERLAY = (15, 20, 30)


# ---------------------------------------------------------------------------
# Core Logic Functions (Testable & Used by Game Loop)
# ---------------------------------------------------------------------------
def move_player(player_x: int, key: int, score: int = 0) -> tuple[int, str]:
    """
    Move the player car left/right by 10 px per key press and keep it inside
    the road boundaries (x = 50 to x = 310 for a 40px-wide car on road 50..350).
    Returns (updated_x, status_message).
    """
    if key == pygame.K_LEFT:
        if player_x <= MIN_CAR_X:
            player_x = MIN_CAR_X
            msg = f"Player car x = {player_x} (no movement, stays on road)"
        else:
            player_x = max(MIN_CAR_X, player_x - PLAYER_STEP)
            msg = f"Player car x = {player_x} | Score: {score} | Game running"
    elif key == pygame.K_RIGHT:
        if player_x >= MAX_CAR_X:
            player_x = MAX_CAR_X
            msg = f"Player car x = {player_x} (no movement, stays on road)"
        else:
            player_x = min(MAX_CAR_X, player_x + PLAYER_STEP)
            msg = f"Player car x = {player_x} | Score: {score} | Game running"
    else:
        msg = f"Key ignored. Player car x = {player_x} | Game running"

    return player_x, msg


def spawn_obstacle(custom_x: int | None = None, custom_y: int = -CAR_HEIGHT) -> pygame.Rect:
    """
    Spawn an obstacle car of size 40x80 at a random x position inside the road.
    """
    x_pos = custom_x if custom_x is not None else random.randint(MIN_CAR_X, MAX_CAR_X)
    return pygame.Rect(x_pos, custom_y, CAR_WIDTH, CAR_HEIGHT)


def check_collision(player_rect: pygame.Rect, obstacle_rect: pygame.Rect) -> bool:
    """
    Detect collision between player car and obstacle car using Rect.colliderect().
    """
    return bool(player_rect.colliderect(obstacle_rect))


def update_obstacles(
    obstacles: list[pygame.Rect],
    player_rect: pygame.Rect,
    score: int,
    speed: int = OBSTACLE_SPEED,
) -> tuple[int, bool, list[str]]:
    """
    Move obstacle cars downwards, increment score when an obstacle leaves the
    screen (y >= 600), and detect collisions with the player car.
    Returns (updated_score, game_over, event_messages).
    """
    messages: list[str] = []
    remaining: list[pygame.Rect] = []
    game_over = False

    for obs in obstacles:
        obs.y += speed

        if check_collision(player_rect, obs):
            game_over = True
            messages.append(f"Collision detected | Game Over | Final Score: {score}")
            remaining.append(obs)
        elif obs.y >= WINDOW_HEIGHT:
            score += 1
            messages.append(f"Obstacle passed. Score: {score}")
        else:
            remaining.append(obs)

    obstacles[:] = remaining
    return score, game_over, messages


def run_test_cases() -> None:
    """
    Run and print the 4 official test cases specified in PS No. 57.
    """
    print("=" * 68)
    print("PS No. 57: Car Racing Game - Official Test Case Verification")
    print("=" * 68)

    # Test Case 1: Normal Input
    _, out1 = move_player(180, pygame.K_RIGHT, score=0)
    print("\n[Test Case 1: Normal Input]")
    print("  Input : Player car x = 180, Key pressed: RIGHT arrow")
    print(f"  Output: {out1}")

    # Test Case 2: Boundary / Minimum Input
    _, out2a = move_player(50, pygame.K_LEFT, score=0)
    _, out2b = move_player(310, pygame.K_RIGHT, score=0)
    print("\n[Test Case 2: Boundary / Minimum Input]")
    print("  Input (a) : Player car x = 50 (left edge of road), key: LEFT arrow")
    print(f"  Output (a): (a) {out2a}")
    print("  Input (b) : Player car x = 310 (right edge of road), key: RIGHT arrow")
    print(f"  Output (b): (b) {out2b}")

    # Test Case 3: Invalid Input
    _, out3 = move_player(180, pygame.K_SPACE, score=0)
    print("\n[Test Case 3: Invalid Input]")
    print("  Input : Player car x = 180, Key pressed: SPACE (not a control key)")
    print(f"  Output: {out3}")

    # Test Case 4: Different Valid Scenario
    score = 3
    player_rect = pygame.Rect(180, 500, CAR_WIDTH, CAR_HEIGHT)
    # (a) Obstacle at (300, 600) leaves the screen
    obs_list_a = [pygame.Rect(300, 600, CAR_WIDTH, CAR_HEIGHT)]
    score, _, msgs_a = update_obstacles(obs_list_a, player_rect, score, speed=0)
    # (b) Obstacle at (200, 520) while player car is at (180, 500)
    obs_list_b = [pygame.Rect(200, 520, CAR_WIDTH, CAR_HEIGHT)]
    score, _, msgs_b = update_obstacles(obs_list_b, player_rect, score, speed=0)

    print("\n[Test Case 4: Different Valid Scenario]")
    print("  Input : Starting score: 3")
    print("          (a) Obstacle at (300, 600) leaves the screen")
    print("          (b) Obstacle at (200, 520) while player car is at (180, 500)")
    print(f"  Output (a): (a) {msgs_a[0]}")
    print(f"  Output (b): (b) {msgs_b[0]}")
    print("=" * 68)


# ---------------------------------------------------------------------------
# Rendering Helpers for Pygame Window
# ---------------------------------------------------------------------------
def draw_car(surface: pygame.Surface, rect: pygame.Rect, body_color: tuple, roof_color: tuple) -> None:
    """Draw a stylized 40x80 2D top-down car inside its exact 40x80 collision Rect."""
    pygame.draw.rect(surface, body_color, rect, border_radius=6)
    # Wheels
    wheel_offsets = [(-3, 10, 4, 16), (rect.width - 1, 10, 4, 16),
                     (-3, rect.height - 26, 4, 16), (rect.width - 1, rect.height - 26, 4, 16)]
    for ox, oy, ww, wh in wheel_offsets:
        pygame.draw.rect(surface, COLOR_WHEEL, (rect.x + ox, rect.y + oy, ww, wh), border_radius=2)
    # Cabin / windshield
    cabin = pygame.Rect(rect.x + 6, rect.y + 18, rect.width - 12, rect.height - 36)
    pygame.draw.rect(surface, roof_color, cabin, border_radius=4)


def draw_scene(
    screen: pygame.Surface,
    player_rect: pygame.Rect,
    obstacles: list[pygame.Rect],
    score: int,
    game_over: bool,
    lane_offset: int,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
) -> None:
    """Draw the road (x = 50 to 350), lane markings, player car, obstacles, HUD, and Game Over screen."""
    # Grass background
    screen.fill(COLOR_GRASS)

    # Road surface (x = 50 to 350, width = 300)
    pygame.draw.rect(screen, COLOR_ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, WINDOW_HEIGHT))

    # Solid road boundary lines at x = 50 and x = 350
    pygame.draw.line(screen, COLOR_BORDER, (ROAD_LEFT, 0), (ROAD_LEFT, WINDOW_HEIGHT), 4)
    pygame.draw.line(screen, COLOR_BORDER, (ROAD_RIGHT, 0), (ROAD_RIGHT, WINDOW_HEIGHT), 4)

    # Dashed lane dividers at x = 150 and x = 250
    for lane_x in (150, 250):
        for y in range(-40, WINDOW_HEIGHT, 60):
            dash_y = y + (lane_offset % 60)
            pygame.draw.rect(screen, COLOR_LANE_LINE, (lane_x - 2, dash_y, 4, 32))

    # Draw obstacle cars (40x80)
    for obs in obstacles:
        draw_car(screen, obs, COLOR_OBSTACLE, COLOR_OBSTACLE_ROOF)

    # Draw player car (40x80 at y = 500)
    draw_car(screen, player_rect, COLOR_PLAYER, COLOR_PLAYER_ROOF)

    # HUD Score banner
    score_surf = font.render(f"Score: {score}", True, COLOR_TEXT)
    pos_surf = font.render(f"Player x: {player_rect.x}", True, COLOR_TEXT)
    screen.blit(score_surf, (65, 14))
    screen.blit(pos_surf, (235, 14))

    # Game Over overlay
    if game_over:
        banner = pygame.Rect(40, 200, 320, 190)
        pygame.draw.rect(screen, COLOR_OVERLAY, banner, border_radius=10)
        pygame.draw.rect(screen, COLOR_BORDER, banner, width=2, border_radius=10)

        over_text = big_font.render("GAME OVER", True, (255, 90, 90))
        final_text = font.render(f"Final Score: {score}", True, COLOR_TEXT)
        restart_text = font.render("Press R to Restart or Q to Quit", True, (200, 220, 255))

        screen.blit(over_text, (WINDOW_WIDTH // 2 - over_text.get_width() // 2, 228))
        screen.blit(final_text, (WINDOW_WIDTH // 2 - final_text.get_width() // 2, 282))
        screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 330))

    pygame.display.flip()


# ---------------------------------------------------------------------------
# Main Game Loop (60 FPS, 400x600 Window)
# ---------------------------------------------------------------------------
def main() -> None:
    """Initialize Pygame and run the 60 FPS Car Racing Game loop."""
    run_test_cases()

    if "--test-only" in sys.argv:
        return

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PS No. 57 - Car Racing Game")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 20, bold=True)
    big_font = pygame.font.SysFont("arial", 36, bold=True)

    # Initial game state
    player_rect = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, CAR_WIDTH, CAR_HEIGHT)
    obstacles: list[pygame.Rect] = []
    score = 0
    game_over = False
    frame_count = 0
    lane_offset = 0

    print("\nStarting interactive 400x600 Pygame window at 60 FPS...")
    print("Controls: LEFT/RIGHT Arrow Keys to steer | R to Restart | ESC/Close to Quit\n")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (game_over and event.key == pygame.K_q):
                    running = False
                elif game_over and event.key == pygame.K_r:
                    # Restart game with R key (Requirement #5)
                    player_rect.x = PLAYER_START_X
                    player_rect.y = PLAYER_START_Y
                    obstacles.clear()
                    score = 0
                    game_over = False
                    frame_count = 0
                    print("Game restarted! Player car x = 180 | Score: 0 | Game running")
                elif not game_over:
                    new_x, msg = move_player(player_rect.x, event.key, score)
                    player_rect.x = new_x
                    print(msg)

        if not game_over:
            frame_count += 1
            lane_offset += OBSTACLE_SPEED

            if frame_count % SPAWN_INTERVAL_FRAMES == 0:
                obstacles.append(spawn_obstacle())

            score, game_over, events = update_obstacles(obstacles, player_rect, score)
            for ev_msg in events:
                print(ev_msg)

        draw_scene(screen, player_rect, obstacles, score, game_over, lane_offset, font, big_font)

    pygame.quit()


if __name__ == "__main__":
    main()