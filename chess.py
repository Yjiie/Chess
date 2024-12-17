import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Инициализация микшера для звука
pygame.mixer.init()

# Размеры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Размеры шахматной доски и клеток
PANEL_WIDTH = 200  # Ширина боковой панели
BOARD_WIDTH = WINDOW_WIDTH - PANEL_WIDTH  # Ширина доски с учетом панели
SQUARE_SIZE = BOARD_WIDTH // 8  # Размер клетки, пропорциональный ширине доски

# Создаем окно с фиксированными размерами
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Шахматы - Король и Ферзь против Короля и Ферзя")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (211, 211, 211)  # Светло-серый цвет
DARK_GRAY = (169, 169, 169)  # Темно-серый цвет
HIGHLIGHT = (0, 255, 0)  # Зеленый для подсветки возможных ходов
PANEL_COLOR = (50, 50, 50)
BUTTON_COLOR = (100, 150, 100)
BUTTON_HOVER_COLOR = (120, 180, 120)

# Шрифт для отображения текста
font = pygame.font.Font(None, 24)

# Загрузка изображений фигур
king_white_img = pygame.image.load("C:/Users/dmitr/OneDrive\Рабочий стол\аисд\Chess\king_white.png")
king_black_img = pygame.image.load("C:/Users\dmitr\OneDrive\Рабочий стол\аисд\Chess\king_black.png")
queen_white_img = pygame.image.load("C:/Users\dmitr\OneDrive\Рабочий стол\аисд\Chess\queen_white.png")
queen_black_img = pygame.image.load("C:/Users\dmitr\OneDrive\Рабочий стол\аисд\Chess\queen_black.png")

# Масштабируем изображения до нужного размера
king_white_img = pygame.transform.scale(king_white_img, (SQUARE_SIZE, SQUARE_SIZE))
king_black_img = pygame.transform.scale(king_black_img, (SQUARE_SIZE, SQUARE_SIZE))
queen_white_img = pygame.transform.scale(queen_white_img, (SQUARE_SIZE, SQUARE_SIZE))
queen_black_img = pygame.transform.scale(queen_black_img, (SQUARE_SIZE, SQUARE_SIZE))

# Загрузка звука для хода
move_sound = pygame.mixer.Sound("C:/Users\dmitr\OneDrive\Рабочий стол\аисд\Chess\move_sound.wav")

# Функция для рисования шахматной доски
def draw_board():
    # Рисуем доску, чередуя светлые и темные клетки
    for row in range(8):
        for col in range(8):
            color = LIGHT_GRAY if (row + col) % 2 == 0 else DARK_GRAY
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Функция для отображения фигур на доске
def draw_pieces(board):
    # Отображаем каждую фигуру на доске в соответствующем месте
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "KW":  # Король белый
                screen.blit(king_white_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif piece == "KB":  # Король черный
                screen.blit(king_black_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif piece == "QW":  # Ферзь белый
                screen.blit(queen_white_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif piece == "QB":  # Ферзь черный
                screen.blit(queen_black_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Функция для подсветки клетки
def highlight_square(row, col):
    # Подсвечиваем выбранную клетку (например, для выделения фигуры)
    pygame.draw.rect(screen, HIGHLIGHT, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

# Проверка допустимости хода (упрощенная)
def is_valid_move(piece, start_row, start_col, end_row, end_col):
    # Проверяем допустимость хода в зависимости от типа фигуры
    if piece.startswith("K"):  # Для короля
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
    elif piece.startswith("Q"):  # Для ферзя
        return start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col)
    return False

# Проверка шаха, мата или пата (с подробностями)
def check_game_status(board, current_turn):
    opponent_turn = "black" if current_turn == "white" else "white"
    king = "KW" if current_turn == "white" else "KB"
    king_pos = None

    # Находим позицию короля
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                king_pos = (row, col)
                break

    if not king_pos:
        return f"Мат. Победили {'Черные' if current_turn == 'white' else 'Белые'}"

    # Проверка, находится ли король под шахом
    in_check = False
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece[1] != king[1]:
                if is_valid_move(piece, row, col, king_pos[0], king_pos[1]):
                    in_check = True

    # Проверка, есть ли допустимые ходы у текущего игрока
    has_valid_moves = False
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and ((current_turn == "white" and piece[1] == "W") or (current_turn == "black" and piece[1] == "B")):
                for r in range(8):
                    for c in range(8):
                        if is_valid_move(piece, row, col, r, c) and board[r][c] == "":
                            has_valid_moves = True
                            break
                if has_valid_moves:
                    break

    # Если нет допустимых ходов
    if not has_valid_moves:
        if in_check:
            return f"Мат. Победили {'Черные' if current_turn == 'white' else 'Белые'}"
        else:
            return "Пат"

    if in_check:
        return f"Шах {'Белым' if current_turn == 'white' else 'Черным'}"

    return None

# Функция для вывода окна победы
def show_victory_window(message):
    victory_window = pygame.Surface((400, 250))
    victory_window.fill(LIGHT_GRAY)

    title_font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 28)

    text = title_font.render(message, True, BLACK)
    new_game_button = pygame.Rect(100, 140, 200, 40)
    exit_button = pygame.Rect(100, 190, 200, 40)

    pygame.draw.rect(victory_window, BUTTON_COLOR, new_game_button)
    pygame.draw.rect(victory_window, BUTTON_COLOR, exit_button)

    new_game_text = button_font.render("Новая игра", True, WHITE)
    exit_text = button_font.render("Выход", True, WHITE)

    victory_window.blit(text, (200 - text.get_width() // 2, 50))
    victory_window.blit(new_game_text, (new_game_button.centerx - new_game_text.get_width() // 2, new_game_button.centery - new_game_text.get_height() // 2))
    victory_window.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))

    while True:
        screen.blit(victory_window, (200, 175))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if new_game_button.collidepoint(pos[0] - 200, pos[1] - 175):
                    return "new_game"
                if exit_button.collidepoint(pos[0] - 200, pos[1] - 175):
                    pygame.quit()
                    sys.exit()

# Функция для отрисовки боковой панели
def draw_sidebar(current_turn, status_message):
    # Рисуем боковую панель с информацией о текущем ходе и статусе игры
    pygame.draw.rect(screen, PANEL_COLOR, pygame.Rect(BOARD_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT))

    # Очередность хода
    turn_text = font.render(f"Ход: {'Белые' if current_turn == 'white' else 'Черные'}", True, WHITE)
    screen.blit(turn_text, (BOARD_WIDTH + 20, 20))

    # Сообщение о статусе игры
    if status_message:
        status_text = font.render(status_message, True, WHITE)
        screen.blit(status_text, (BOARD_WIDTH + 20, 60))

    # Кнопка "Согласиться на пат"
    pat_button = pygame.Rect(BOARD_WIDTH + 20, 100, 160, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, pat_button)
    pat_text = font.render("Согласиться на пат", True, WHITE)
    screen.blit(pat_text, (BOARD_WIDTH + 21, 110))

    # Кнопка "Выход из игры"
    exit_button = pygame.Rect(BOARD_WIDTH + 20, 160, 160, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, exit_button)
    exit_text = font.render("Выход из игры", True, WHITE)
    screen.blit(exit_text, (BOARD_WIDTH + 35, 170))

    return pat_button, exit_button

# Основной игровой экран
def game_screen():
    # Инициализация пустой доски
    board = [["" for _ in range(8)] for _ in range(8)]
    board[random.randint(0, 7)][random.randint(0, 7)] = "KW"
    board[random.randint(0, 7)][random.randint(0, 7)] = "QW"
    board[random.randint(0, 7)][random.randint(0, 7)] = "KB"
    board[random.randint(0, 7)][random.randint(0, 7)] = "QB"

    selected_piece = None  # Фигура, выбранная для перемещения
    selected_position = None  # Позиция выбранной фигуры
    current_turn = "white"  # Очередность хода
    status_message = "Новая игра начата"  # Статус игры

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Проверяем статус игры на каждом кадре
        status_message = check_game_status(board, current_turn)
        if status_message and "Победили" in status_message:
            result = show_victory_window(status_message)
            if result == "new_game":
                return game_screen()
            else:
                running = False

        draw_board()
        draw_pieces(board)
        pat_button, exit_button = draw_sidebar(current_turn, status_message)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                if row < 8 and col < 8:  # Убедимся, что клик внутри доски
                    if selected_piece:
                        # Проверяем возможность хода
                        if is_valid_move(selected_piece, selected_position[0], selected_position[1], row, col):
                            board[selected_position[0]][selected_position[1]] = ""
                            board[row][col] = selected_piece
                            selected_piece = None
                            selected_position = None

                            # Переключаем ход
                            current_turn = "black" if current_turn == "white" else "white"

                            # Воспроизводим звук
                            move_sound.play()

                        else:
                            selected_piece = None
                            selected_position = None
                    elif board[row][col]:
                        # Выбираем фигуру
                        piece = board[row][col]
                        if (current_turn == "white" and piece[1] == "W") or (current_turn == "black" and piece[1] == "B"):
                            selected_piece = piece
                            selected_position = (row, col)
                
                # Обработка кнопок
                if pat_button.collidepoint(pos[0] - BOARD_WIDTH, pos[1]):
                    status_message = "Пат. Игра закончена!"
                    show_victory_window("Ничья!")
                    return

                if exit_button.collidepoint(pos[0] - BOARD_WIDTH, pos[1]):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Проверка нажатия на кнопку "Согласиться на пат"
                if BOARD_WIDTH + 20 <= pos[0] <= BOARD_WIDTH + 180 and 100 <= pos[1] <= 140:
                    result = show_victory_window("Игра завершилась вничью (пат)")
                    if result == "new_game":
                        return game_screen()
                    else:
                        running = False
                # Проверка нажатия на кнопку "Выход из игры"
                if BOARD_WIDTH + 20 <= pos[0] <= BOARD_WIDTH + 180 and 160 <= pos[1] <= 200:
                    pygame.quit()
                    sys.exit()       
                
            # Подсветка выбранной фигуры
            if selected_position:
                highlight_square(*selected_position)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    game_screen()
    pygame.quit()
    sys.exit()
