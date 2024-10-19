import os
import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Antivirus Scanner")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# List of known malware signatures (for demonstration)
MALWARE_SIGNATURES = [
    b'malicious_file_signature_1',
    b'malicious_file_signature_2',
]

# Directory to scan for suspicious files
scan_directory = "C:/Users/junch/Documents"  # Change this to your desired directory


def scan_file(file_path):
    """Scan a single file for malware signatures."""
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            for signature in MALWARE_SIGNATURES:
                if signature in file_content:
                    return True  # Malware found
    except Exception:
        pass  # Ignore errors
    return False  # No malware found


def get_recent_suspicious_files(directory, num_files=5):
    """Get the most recently modified suspicious files in the specified directory."""
    suspicious_extensions = ['.exe', '.scr', '.bat', '.cmd', '.vbs']  # Add more suspicious extensions as needed
    files_with_time = [
        (os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f)))
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith(tuple(suspicious_extensions))
    ]

    # Sort files by modification time (most recent first)
    recent_files = sorted(files_with_time, key=lambda x: x[1], reverse=True)

    # Return the most recent files
    return [file[0] for file in recent_files[:num_files]]


# Main loop
running = True
result_text = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the most recent suspicious files
    recent_files = get_recent_suspicious_files(scan_directory)

    # Scan the recent files
    virus_found = any(scan_file(file) for file in recent_files)
    result_text = "VIRUS!" if virus_found else "CLEAR!"

    # Fill the screen with white
    screen.fill(WHITE)

    # Render the result
    font = pygame.font.Font(None, 74)
    text = font.render(result_text, True, RED if virus_found else GREEN)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

# Clean up
pygame.quit()
