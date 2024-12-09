import pygame
import random
import time

# Constants for Game States
START_SCREEN = 0
CHOOSE_DIFFICULTY = 1
GAME_PLAY = 2
GAME_OVER = 3
FEEDBACK = 4

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Guessing Game")

# Colors
background_color = (255, 255, 200)  # pastel yellow
button_color = (100, 200, 255)
text_color = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 40)

# Game variables
game_state = START_SCREEN
selected_difficulty = None
score = 0
running = True
correct_answer = None
answer_choices = []
feedback_text = ""
feedback_start_time = 0  # Start time for feedback timer
song_played = False  # Flag to check if the song has already been played
songs_played = 0  # Counter to track number of songs played
played_songs = []  # List to keep track of songs that have already been played

# Buttons
start_button = pygame.Rect(300, 250, 200, 50)
easy_button = pygame.Rect(200, 300, 100, 50)
medium_button = pygame.Rect(340, 300, 125, 50)
hard_button = pygame.Rect(500, 300, 100, 50)
play_again_button = pygame.Rect(300, 350, 200, 50)  # Play Again button
logo = pygame.image.load(r'C:\Users\janet\Downloads\Pictures in Math 153\Vortex-removebg-preview.png')
logo = pygame.transform.scale(logo, (200, 100))

# Simple song data (File paths should be accurate)
songs = {
    'easy': [
        {'Song': 'Awitin Mo at Isasayaw Ko', 'Artist': 'VST & Company', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Awitin_mo_e.mp3'},
        {'Song': 'Ang Huling El Bimbo', 'Artist': 'Eraserheads', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\El_bimbo_e.mp3'},
        {'Song': 'Panalangin', 'Artist': 'Apo Hiking Society', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Panalangin_e.mp3'},
        {'Song': 'Kahit Maputi Na Ang Buhok Ko', 'Artist': 'Rey Valera', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Kahit_maputi_e.mp3'},
        {'Song': 'Urong-Sulong', 'Artist': 'Bea Benene', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\urong_sulong_e.mp3'},
        {'Song': 'Torete', 'Artist': 'Moonstar88', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\torete_e.mp3'}
    ],
    'medium': [
        {'Song': 'This Guy\'s In Love With You Pare', 'Artist': 'Parokya ni Edgar', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\This_guy_inlove_m.mp3'},
        {'Song': 'Pag-ibig', 'Artist': 'Sponge Cola', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\pag-ibig_m.mp3'},
        {'Song': 'Narda', 'Artist': 'Kamikazee', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Narda_m.mp3'},
        {'Song': 'Harana', 'Artist': 'Parokya ni Edgar', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\harana_m.mp3'},
        {'Song': 'Buloy', 'Artist': 'Parokya ni Edgar', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\buloy_m.mp3'},
        {'Song': 'Ako\'y Tinamaan', 'Artist': 'Reo Brothers', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Akoy_ay_tinamaan_m.mp3'}
    ],
    'hard': [
        {'Song': 'Buko', 'Artist': 'Jireh Lim', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Buko_d.mp3'},
        {'Song': 'Ang Kawawang Cowboy', 'Artist': 'Fred Panopio', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Ang_Kawawang_Cowboy_d.mp3'},
        {'Song': 'Sa Isang Sulyap Mo', 'Artist': '1:30', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Sa_isang_sulyap_mo_d.mp3'},
        {'Song': 'Diwata', 'Artist': 'Abra', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\diwata_d.mp3'},
        {'Song': 'Gitara', 'Artist': 'Parokya ni Edgar', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Gitara_d.mp3'},
        {'Song': 'Ngiti', 'Artist': 'Ronnie Liang', 'File': r'C:\Users\janet\Downloads\Musics in Math 153\Ngiti_d.mp3'}
    ]
}

# Function to return a comment based on the score
def get_score_comment(score):
    if score == 1:
        return "You can try again"
    elif score == 2:
        return "Good job!"
    elif score == 3:
        return "Fantastic!"
    elif score == 4:
        return "Very good!"
    elif score >= 5:
        return "Perfect!"
    else:
        return ""

# Function to play a random song based on the selected difficulty
def play_random_song(difficulty):
    if difficulty not in songs:  # Corrected from 'song' to 'songs'
        print(f"Error: Invalid difficulty selected '{difficulty}'")
        return None
    
    available_songs = [song for song in songs[difficulty] if song['Song'] not in played_songs]
    
    if not available_songs:  # All songs have been played
        played_songs.clear()  # Reset played songs list
        available_songs = songs[difficulty]  # Reset to all songs

    return random.choice(available_songs)  # Select a random song

# Function to generate answer choices (3 total: 1 correct, 2 incorrect)
def generate_choices(correct_answer, difficulty):
    all_songs = [song['Song'] for song in songs[difficulty]]
    choices = [correct_answer]
    
    while len(choices) < 3:
        random_choice = random.choice(all_songs)
        if random_choice not in choices:
            choices.append(random_choice)
    
    random.shuffle(choices)  # Shuffle the choices
    return choices

# Reset the game
def reset_game():
    global score, songs_played, played_songs, game_state, selected_difficulty, correct_answer, answer_choices, feedback_text, song_played
    score = 0
    songs_played = 0
    played_songs.clear()
    song_played = False
    feedback_text = ""
    game_state = START_SCREEN
    selected_difficulty = None
    correct_answer = None
    answer_choices = []

# Event handling and main game loop
while running:
    gameWindow.fill(background_color)

    if game_state == START_SCREEN:
        gameWindow.blit(logo, (WIDTH // 2 - 100, 50))  # Draw logo
        pygame.draw.rect(gameWindow, button_color, start_button)
        text = font.render('Play', True, text_color)
        gameWindow.blit(text, (start_button.x + 70, start_button.y + 10))

    elif game_state == CHOOSE_DIFFICULTY:
        # Draw logo at the top of the screen
        gameWindow.blit(logo, (WIDTH // 2 - 100, 50))  # Draw logo
        pygame.draw.rect(gameWindow, button_color, easy_button)
        pygame.draw.rect(gameWindow, button_color, medium_button)
        pygame.draw.rect(gameWindow, button_color, hard_button)

        gameWindow.blit(font.render('Easy', True, text_color), (easy_button.x + 20, easy_button.y + 10))
        gameWindow.blit(font.render('Medium', True, text_color), (medium_button.x + 10, medium_button.y + 10))
        gameWindow.blit(font.render('Hard', True, text_color), (hard_button.x + 18, hard_button.y + 10))

    elif game_state == GAME_PLAY:
        if not song_played:
            current_song = play_random_song(selected_difficulty)
            if current_song is None:
                continue

            correct_answer = current_song['Song']
            answer_choices = generate_choices(correct_answer, selected_difficulty)

            try:
                pygame.mixer.music.load(current_song['File'])
                pygame.mixer.music.play()
                song_played = True
                played_songs.append(correct_answer)
            except pygame.error as e:
                print(f"Error loading file: {e}")
                continue

        button_height = 50
        button_width = 500
        choices_y = 200
        for i, choice in enumerate(answer_choices):
            choice_button = pygame.Rect(150, choices_y + i * (button_height + 10), button_width, button_height)
            pygame.draw.rect(gameWindow, button_color, choice_button)
            gameWindow.blit(font.render(choice, True, text_color), (choice_button.x + 10, choice_button.y + 10))

        score_text = f"Score: {score}"
        gameWindow.blit(font.render(score_text, True, text_color), (WIDTH - 150, 20))

        if songs_played >= 5:  # 5 rounds of songs before game over
            game_state = GAME_OVER

    elif game_state == FEEDBACK:
        gameWindow.blit(font.render(feedback_text, True, text_color), (WIDTH // 4, HEIGHT // 2))
        current_time = pygame.time.get_ticks()
        if current_time - feedback_start_time > 1000:
            game_state = GAME_PLAY
            song_played = False

    elif game_state == GAME_OVER:
        gameWindow.blit(font.render(f"Game Over! Final Score: {score}", True, text_color), (WIDTH // 3, HEIGHT // 3))
        gameWindow.blit(font.render(get_score_comment(score), True, text_color), (WIDTH // 3, HEIGHT // 3 + 50))
        pygame.draw.rect(gameWindow, button_color, play_again_button)
        gameWindow.blit(font.render('Play Again', True, text_color), (play_again_button.x + 30, play_again_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(pos):
                    reset_game()  # Reset the game when the player clicks 'Play Again'
                    game_state = START_SCREEN  # Go back to the start screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Start Screen Button
            if game_state == START_SCREEN and start_button.collidepoint(pos):
                game_state = CHOOSE_DIFFICULTY

            # Difficulty Selection
            if game_state == CHOOSE_DIFFICULTY:
                if easy_button.collidepoint(pos):
                    selected_difficulty = 'easy'
                    game_state = GAME_PLAY
                elif medium_button.collidepoint(pos):
                    selected_difficulty = 'medium'
                    game_state = GAME_PLAY
                elif hard_button.collidepoint(pos):
                    selected_difficulty = 'hard'
                    game_state = GAME_PLAY

            # Answer choices
            if game_state == GAME_PLAY:
                for i, choice in enumerate(answer_choices):
                    choice_button = pygame.Rect(150, 200 + i * (50 + 10), 500, 50)
                    if choice_button.collidepoint(pos):
                        if choice == correct_answer:
                            score += 1
                            feedback_text = "Correct!"
                        else:
                            feedback_text = f"Wrong! The correct answer was: {correct_answer}"

                        feedback_start_time = pygame.time.get_ticks()
                        game_state = FEEDBACK
                        song_played = False
                        songs_played += 1

    pygame.display.update()

pygame.quit()
