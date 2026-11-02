# PS No. 57: Car Racing Game (Python & Pygame)

**University:** Rungta International Skills University — School of Information Technology  
**Program:** Bachelor of Computer Application (BCA) — First Semester, Section 1A  
**Course:** Programming Fundamentals Using Python (`RU-100-05-00058`)  
**Student Name:** Manav Kumar Singh  ERP-RU-26-01445
**Repository:** [manavkumarsingh-star/BCA-python-project](https://www.google.com/search?q=https://github.com/manavkumarsingh-star/BCA-python-project)

## 1. Problem Statement

Create a 2D car racing game in which the player steers a car left and right on a road using the arrow keys, avoids obstacle cars coming down from the top, and scores a point for every obstacle passed. The game ends when the player's car collides with an obstacle.

| Parameter | Specification |
| :--- | :--- |
| **Language & Library** | Python 3, `pygame` |
| **Core Concepts** | Pygame Window & Rendering, `Rect.colliderect()` Collision Detection, 60 FPS Game Loop |
| **Window Dimensions** | `400 x 600` pixels |
| **Road Boundaries** | `x = 50` to `x = 350` (width `300 px`) |
| **Player Car** | `40 x 80` pixels at `y = 500`, starting `x = 180`, moves `10 px` per arrow key press |
| **Valid Player X Range** | `x = 50` (left road edge) to `x = 310` (`310 + 40 = 350`, right road edge) |
| **Obstacle Cars** | `40 x 80` pixels spawning at random `x` within `[50, 310]` and moving downwards |
| **Scoring & Restart** | `+1` point per obstacle passed (`y >= 600`); collision triggers `Game Over`; `R` key restarts |

## 2. Project Files in This Repository

| File Name | Description |
| :--- | :--- |
| `car_racing_game.py` | Complete single-file Python 3 solution with 60 FPS Pygame loop and built-in test case verifier |
| `Project_Report_PS57.pdf` | Formal project documentation and test case evaluation report |
| `requirements.txt` | Python package dependency list (`pygame`) |
| `README.md` | Project documentation, setup instructions, controls, and test results |

## 3. Installation & How to Run

1. **Clone the repository (or download the files):**
   ```bash
   git clone https://github.com/manavkumarsingh-star/BCA-python-project.git
   cd BCA-python-project
   ```

2. **Install Pygame:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game from the console:**
   ```bash
   python car_racing_game.py
   ```

4. **Run automated test case verification only (console mode):**
   ```bash
   python car_racing_game.py --test-only
   ```

## 4. Game Controls

| Key | Action |
| :--- | :--- |
| `LEFT Arrow` | Move player car `10 px` left (clamped at left road edge `x = 50`) |
| `RIGHT Arrow` | Move player car `10 px` right (clamped at right road edge `x = 310`) |
| `R` | Restart the game from the `Game Over` screen |
| `ESC` / `Q` | Quit the game window |

## 5. Official Test Cases & Verified Outputs

| Test Case | Input Scenario | Expected & Verified Console Output |
| :--- | :--- | :--- |
| **Test Case 1: Normal Input** | Player car `x = 180`; Key pressed: `RIGHT arrow` | `Player car x = 190 \| Score: 0 \| Game running` |
| **Test Case 2: Boundary / Minimum Input** | (a) Player car `x = 50`, key: `LEFT arrow`<br>(b) Player car `x = 310`, key: `RIGHT arrow` | (a) `Player car x = 50 (no movement, stays on road)`<br>(b) `Player car x = 310 (no movement, stays on road)` |
| **Test Case 3: Invalid Input** | Player car `x = 180`; Key pressed: `SPACE` | `Key ignored. Player car x = 180 \| Game running` |
| **Test Case 4: Different Valid Scenario** | Starting score: `3`<br>(a) Obstacle at `(300, 600)` leaves screen<br>(b) Obstacle at `(200, 520)` while player at `(180, 500)` | (a) `Obstacle passed. Score: 4`<br>(b) `Collision detected \| Game Over \| Final Score: 4` |
