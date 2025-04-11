#!/usr/bin/env python3
"""
Terminal Snake Game

A classic snake game implemented with Python's curses library.
Use arrow keys to move the snake. Eat food to grow longer.
Game ends when the snake hits the wall or itself.
"""

import curses
import random
import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.timeout(100)  # Refresh rate in milliseconds
    
    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    
    # Check if terminal is large enough
    if sh < 10 or sw < 30:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small. Resize and try again.")
        stdscr.refresh()
        time.sleep(2)
        return
    
    # Create a game window with a border
    win = curses.newwin(sh-2, sw-2, 1, 1)
    win.keypad(1)
    win.timeout(100)
    
    # Get game area dimensions (accounting for border)
    h, w = win.getmaxyx()
    
    # Initialize snake
    snake_x = w // 4
    snake_y = h // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # Initial snake direction
    direction = KEY_RIGHT
    
    # Create initial food
    food = create_food(h, w, snake)
    win.addch(food[0], food[1], curses.ACS_DIAMOND)
    
    # Score tracking
    score = 0
    
    # Draw border
    stdscr.box()
    stdscr.addstr(0, sw//2 - 5, " SNAKE GAME ")
    stdscr.refresh()
    
    # Show instructions
    show_instructions(stdscr, sh, sw)
    
    # Game loop
    while True:
        # Display score
        stdscr.addstr(sh-1, 2, f" Score: {score} ")
        stdscr.refresh()
        
        # Get next key press
        next_key = win.getch()
        
        # If no key is pressed, continue in current direction
        if next_key == -1:
            pass
        # Quit the game if q is pressed
        elif next_key == ord('q'):
            break
        # Otherwise change direction if valid
        else:
            direction = process_key_input(next_key, direction)
        
        # Calculate new head position based on direction
        new_head = calculate_new_head(snake, direction)
        
        # Check for collisions
        if (new_head[0] in [0, h-1] or
            new_head[1] in [0, w-1] or
            new_head in snake):
            # Game over
            if game_over(stdscr, sh, sw, score):
                # Reset game
                win.clear()
                snake = [
                    [snake_y, snake_x],
                    [snake_y, snake_x - 1],
                    [snake_y, snake_x - 2]
                ]
                direction = KEY_RIGHT
                food = create_food(h, w, snake)
                win.addch(food[0], food[1], curses.ACS_DIAMOND)
                score = 0
                continue
            else:
                break
        
        # Move snake (add new head)
        snake.insert(0, new_head)
        
        # Check if snake ate the food
        if snake[0] == food:
            # Create new food
            food = create_food(h, w, snake)
            win.addch(food[0], food[1], curses.ACS_DIAMOND)
            score += 1
        else:
            # Remove tail if no food was eaten
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')
        
        # Draw snake head
        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

def create_food(h, w, snake):
    """Create food at a random position that is not occupied by the snake."""
    while True:
        food = [random.randint(1, h-2), random.randint(1, w-2)]
        if food not in snake:
            return food

def process_key_input(key, current_direction):
    """Process key inputs and return the new direction."""
    # Map key codes to directions
    if key == KEY_DOWN and current_direction != KEY_UP:
        return KEY_DOWN
    elif key == KEY_UP and current_direction != KEY_DOWN:
        return KEY_UP
    elif key == KEY_LEFT and current_direction != KEY_RIGHT:
        return KEY_LEFT
    elif key == KEY_RIGHT and current_direction != KEY_LEFT:
        return KEY_RIGHT
    else:
        return current_direction

def calculate_new_head(snake, direction):
    """Calculate the position of the new head based on the direction."""
    new_head = snake[0].copy()
    if direction == KEY_DOWN:
        new_head[0] += 1
    elif direction == KEY_UP:
        new_head[0] -= 1
    elif direction == KEY_LEFT:
        new_head[1] -= 1
    elif direction == KEY_RIGHT:
        new_head[1] += 1
    return new_head

def show_instructions(stdscr, sh, sw):
    """Display game instructions."""
    instructions = [
        "INSTRUCTIONS:",
        "Use arrow keys to move",
        "Press 'q' to quit",
        "",
        "Press any key to start"
    ]
    
    # Calculate position for instructions
    start_y = sh // 2 - len(instructions) // 2
    start_x = sw // 2 - 12
    
    # Display instructions
    for i, line in enumerate(instructions):
        stdscr.addstr(start_y + i, start_x, line)
    
    stdscr.refresh()
    stdscr.getch()  # Wait for key press

def game_over(stdscr, sh, sw, score):
    """Display game over screen and handle restart."""
    game_over_text = [
        "GAME OVER",
        f"Final Score: {score}",
        "",
        "Press 'r' to restart",
        "Press 'q' to quit"
    ]
    
    # Calculate position for game over text
    start_y = sh // 2 - len(game_over_text) // 2
    start_x = sw // 2 - 10
    
    # Clear screen
    stdscr.clear()
    stdscr.box()
    
    # Display game over text
    for i, line in enumerate(game_over_text):
        stdscr.addstr(start_y + i, start_x, line)
    
    stdscr.refresh()
    
    # Wait for restart or quit
    while True:
        key = stdscr.getch()
        if key == ord('r'):
            return True  # Restart
        elif key == ord('q'):
            return False  # Quit
        
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    finally:
        # Clean up curses
        curses.endwin()
        print("Thanks for playing Snake!")

