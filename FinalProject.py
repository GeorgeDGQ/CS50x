# Jorge Daniel Gómez Quintana Final Project "Mandelbrot & Julia Visualizer"
import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Window configuration
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot and Julia Fractals")

# Fractal parameters
MAX_ITER = 100  # Maximum iterations
ZOOM_FACTOR = 0.8  # Zoom factor
ESCAPE_RADIUS = 2.0  # Escape radius

# Initial region (Mandelbrot)
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5

# Julia parameters (interesting initial value)
c_julia = complex(-0.7, 0.27015)

# Current mode (Mandelbrot or Julia)
fractal_mode = "Mandelbrot"  # or "Julia"

# Color palette
def generate_palette():
    global palette
    palette = []
    r_offset = np.random.randint(0, 256)
    g_offset = np.random.randint(0, 256)
    b_offset = np.random.randint(0, 256)
    for i in range(MAX_ITER):
        r = int((np.sin(0.3 * i + r_offset) * 127 + 128))
        g = int((np.sin(0.3 * i + g_offset) * 127 + 128))
        b = int((np.sin(0.3 * i + b_offset) * 127 + 128))
        palette.append((r, g, b))
    palette.append((0, 0, 0))  # Color for the set

generate_palette()

# Function to compute the value of a pixel
def compute_pixel(x, y):
    if fractal_mode == "Mandelbrot":
        c = complex(x_min + (x / WIDTH) * (x_max - x_min),
                    y_min + (y / HEIGHT) * (y_max - y_min))
        z = 0j
    else:  # Julia
        z = complex(x_min + (x / WIDTH) * (x_max - x_min),
                    y_min + (y / HEIGHT) * (y_max - y_min))
        c = c_julia

    for i in range(MAX_ITER):
        z = z * z + c
        if abs(z) > ESCAPE_RADIUS:
            return i
    return MAX_ITER

# Function to render the fractal
def render_fractal():
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)  # Row, column, channel
    for y in range(HEIGHT):
        for x in range(WIDTH):
            iter_count = compute_pixel(x, y)
            pixels[y, x] = palette[iter_count]
    return pygame.surfarray.make_surface(pixels)

# Function to draw the UI
def draw_ui():
    font = pygame.font.SysFont('Arial', 20)
    # Mode information
    mode_text = font.render(f"Mode: {fractal_mode}", True, (255, 255, 255))
    screen.blit(mode_text, (20, 20))
    # Julia parameters
    if fractal_mode == "Julia":
        julia_text = font.render(f"c = {c_julia.real:.4f} + {c_julia.imag:.4f}i", True, (255, 255, 255))
        screen.blit(julia_text, (20, 50))
    # Iterations
    iter_text = font.render(f"Iterations: {MAX_ITER}", True, (255, 255, 255))
    screen.blit(iter_text, (20, HEIGHT - 30))
    # Instructions
    instructions = [
        "Controls:",
        "M - Switch between Mandelbrot/Julia",
        "Mouse wheel - Zoom",
        "Click and drag - Move view",
        "C - Change color palette",
        "Arrow keys ↑↓ - Increase/Decrease iterations",
        "J/K/L/H - Change Julia parameter (in Julia mode)",
        "R - Reset view"
    ]
    for i, text in enumerate(instructions):
        rendered = font.render(text, True, (255, 255, 200))
        screen.blit(rendered, (WIDTH - 350, 20 + i * 30))

# Render initial fractal
fractal_surface = render_fractal()
screen.blit(fractal_surface, (0, 0))
pygame.display.flip()

# Interaction variables
dragging = False
last_mouse_pos = (0, 0)
last_zoom_center = (0, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
            # Zoom with mouse wheel
            elif event.button == 4 or event.button == 5:  # Wheel up/down
                zoom_in = (event.button == 4)
                last_zoom_center = pygame.mouse.get_pos()
                mouse_x, mouse_y = last_zoom_center
                region_width = x_max - x_min
                region_height = y_max - y_min
                cx = x_min + (mouse_x / WIDTH) * region_width
                cy = y_min + (mouse_y / HEIGHT) * region_height
                if zoom_in:
                    x_min = cx - region_width * ZOOM_FACTOR / 2
                    x_max = cx + region_width * ZOOM_FACTOR / 2
                    y_min = cy - region_height * ZOOM_FACTOR / 2
                    y_max = cy + region_height * ZOOM_FACTOR / 2
                else:
                    x_min = cx - region_width / (ZOOM_FACTOR * 2)
                    x_max = cx + region_width / (ZOOM_FACTOR * 2)
                    y_min = cy - region_height / (ZOOM_FACTOR * 2)
                    y_max = cy + region_height / (ZOOM_FACTOR * 2)
                fractal_surface = render_fractal()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Release left click
                dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                last_x, last_y = last_mouse_pos
                dx = (x_max - x_min) * (last_x - mouse_x) / WIDTH
                dy = (y_max - y_min) * (mouse_y - last_y) / HEIGHT
                x_min += dx
                x_max += dx
                y_min += dy
                y_max += dy
                last_mouse_pos = (mouse_x, mouse_y)
                fractal_surface = render_fractal()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Switch mode
                fractal_mode = "Julia" if fractal_mode == "Mandelbrot" else "Mandelbrot"
                fractal_surface = render_fractal()
            elif event.key == pygame.K_c:  # Change palette
                generate_palette()
                fractal_surface = render_fractal()
            elif event.key == pygame.K_r:  # Reset view
                x_min, x_max = -2.0, 1.0
                y_min, y_max = -1.5, 1.5
                fractal_surface = render_fractal()
            elif event.key == pygame.K_UP:  # Increase iterations
                MAX_ITER += 10
                generate_palette()
                fractal_surface = render_fractal()
            elif event.key == pygame.K_DOWN:  # Decrease iterations
                MAX_ITER = max(20, MAX_ITER - 10)
                generate_palette()
                fractal_surface = render_fractal()
            # Change Julia parameter
            elif fractal_mode == "Julia" and event.key == pygame.K_j:
                c_julia = complex(c_julia.real + 0.01, c_julia.imag)
                fractal_surface = render_fractal()
            elif fractal_mode == "Julia" and event.key == pygame.K_k:
                c_julia = complex(c_julia.real - 0.01, c_julia.imag)
                fractal_surface = render_fractal()
            elif fractal_mode == "Julia" and event.key == pygame.K_l:
                c_julia = complex(c_julia.real, c_julia.imag + 0.01)
                fractal_surface = render_fractal()
            elif fractal_mode == "Julia" and event.key == pygame.K_h:
                c_julia = complex(c_julia.real, c_julia.imag - 0.01)
                fractal_surface = render_fractal()

    # Draw everything
    screen.blit(fractal_surface, (0, 0))
    draw_ui()
    pygame.display.flip()

pygame.quit()
sys.exit()