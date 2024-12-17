import pygame
import sys
import os

# Путь к файлу с данными пользователей
USER_DATA_FILE = "users.txt"

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Авторизация")

# Шрифт
font = pygame.font.Font(None, 24)
error_font = pygame.font.Font(None, 20)

# Загрузка фона
background_image = pygame.image.load("C:/Users\dmitr\OneDrive\Рабочий стол\аисд\Chess/background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Функция для загрузки данных пользователей
def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, "r") as file:
        users = {}
        for line in file:
            if ':' in line:  # Проверяем, есть ли разделитель
                login, password = line.strip().split(":", 1)
                users[login] = password
        return users


# Функция для сохранения данных пользователей
def save_user(login, password):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{login}:{password}\n")

# Экран регистрации нового пользователя
# Экран регистрации нового пользователя
# Экран регистрации нового пользователя
def registration_screen():
    login_text = ''
    password_text = ''
    confirm_password_text = ''

    input_rect_login = pygame.Rect(150, 50, 180, 30)
    input_rect_password = pygame.Rect(150, 100, 180, 30)
    input_rect_confirm_password = pygame.Rect(150, 180, 180, 30)

    active_login = False
    active_password = False
    active_confirm_password = False
    error_message = None
    success_message = None
    clock = pygame.time.Clock()

    # Кнопка возврата к входу
    login_button = pygame.Rect(100, 250, 100, 30)
    # Кнопка сохранения данных
    save_button = pygame.Rect(200, 250, 100, 30)  # Позиционируем кнопку рядом с кнопкой входа

    while True:
        screen.blit(background_image, (0, 0))

        # Полупрозрачный фон для формы регистрации
        transparent_surface = pygame.Surface((WIDTH, HEIGHT))
        transparent_surface.set_alpha(150)  # Устанавливаем прозрачность
        transparent_surface.fill((0, 0, 0))  # Черный цвет
        screen.blit(transparent_surface, (0, 0))

        # Отображение текста "Логин", "Пароль" и "Подтвердите\nПароль"
        login_label = font.render("Логин:", True, (255, 255, 255))
        password_label = font.render("Пароль:", True, (255, 255, 255))
        confirm_password_label1 = font.render("Подтвердите", True, (255, 255, 255))
        confirm_password_label2 = font.render("Пароль:", True, (255, 255, 255))

        screen.blit(login_label, (50, 55))
        screen.blit(password_label, (50, 105))
        screen.blit(confirm_password_label1, (50, 155))  # Первая строка "Подтвердите"
        screen.blit(confirm_password_label2, (50, 185))  # Вторая строка "Пароль"

        login_surface = font.render(login_text, True, (255, 255, 255))
        password_surface = font.render('*' * len(password_text), True, (255, 255, 255))
        confirm_password_surface = font.render('*' * len(confirm_password_text), True, (255, 255, 255))
        screen.blit(login_surface, (input_rect_login.x + 5, input_rect_login.y + 5))
        screen.blit(password_surface, (input_rect_password.x + 5, input_rect_password.y + 5))
        screen.blit(confirm_password_surface, (input_rect_confirm_password.x + 5, input_rect_confirm_password.y + 5))

        pygame.draw.rect(screen, (255, 255, 255), input_rect_login, 2 if active_login else 1)
        pygame.draw.rect(screen, (255, 255, 255), input_rect_password, 2 if active_password else 1)
        pygame.draw.rect(screen, (255, 255, 255), input_rect_confirm_password, 2 if active_confirm_password else 1)

        # Отображение кнопок
        login_label = font.render("Вход", True, (255, 255, 255))
        save_label = font.render("Сохранить", True, (255, 255, 255))
        screen.blit(login_label, (login_button.x + 25, login_button.y + 5))
        screen.blit(save_label, (save_button.x + 10, save_button.y + 5))

        if error_message:
            error_surface = error_font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (50, 280))

        if success_message:
            success_surface = error_font.render(success_message, True, (0, 255, 0))
            screen.blit(success_surface, (50, 280))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect_login.collidepoint(event.pos):
                    active_login = True
                    active_password = False
                    active_confirm_password = False
                elif input_rect_password.collidepoint(event.pos):
                    active_login = False
                    active_password = True
                    active_confirm_password = False
                elif input_rect_confirm_password.collidepoint(event.pos):
                    active_login = False
                    active_password = False
                    active_confirm_password = True
                elif login_button.collidepoint(event.pos):
                    return  # Возврат на экран входа
                elif save_button.collidepoint(event.pos):
                    if not login_text or not password_text or not confirm_password_text:
                        error_message = "Заполните все поля"
                        success_message = None
                    elif password_text != confirm_password_text:
                        error_message = "Пароли не совпадают"
                        success_message = None
                    else:
                        users = load_users()
                        if login_text in users:
                            error_message = "Логин уже существует"
                            success_message = None
                        else:
                            save_user(login_text, password_text)
                            success_message = "Успешная регистрация!"
                            error_message = None
                            login_text = ''
                            password_text = ''
                            confirm_password_text = ''

            if event.type == pygame.KEYDOWN:
                if active_login:
                    if event.key == pygame.K_BACKSPACE:
                        login_text = login_text[:-1]
                    else:
                        login_text += event.unicode

                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode

                if active_confirm_password:
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password_text = confirm_password_text[:-1]
                    else:
                        confirm_password_text += event.unicode

                if event.key == pygame.K_RETURN:
                    if not login_text or not password_text or not confirm_password_text:
                        error_message = "Заполните все поля"
                        success_message = None
                    elif password_text != confirm_password_text:
                        error_message = "Пароли не совпадают"
                        success_message = None
                    else:
                        users = load_users()
                        if login_text in users:
                            error_message = "Логин уже существует"
                            success_message = None
                        else:
                            save_user(login_text, password_text)
                            success_message = "Успешная регистрация!"
                            error_message = None
                            login_text = ''
                            password_text = ''
                            confirm_password_text = ''

        pygame.display.flip()
        clock.tick(30)


    # Кнопка возврата к входу
    login_button = pygame.Rect(150, 250, 100, 30)

    

# Экран входа в систему
def login_screen():
    login_text = ''
    password_text = ''

    input_rect_login = pygame.Rect(150, 70, 180, 30)
    input_rect_password = pygame.Rect(150, 130, 180, 30)

    active_login = False
    active_password = False
    error_message = None
    clock = pygame.time.Clock()

    # Кнопки
    register_button = pygame.Rect(230, 220, 100, 30)
    login_button = pygame.Rect(50, 220, 80, 30)

    while True:
        screen.blit(background_image, (0, 0))

        login_label = font.render("Логин:", True, (255, 255, 255))
        password_label = font.render("Пароль:", True, (255, 255, 255))
        screen.blit(login_label, (50, 75))
        screen.blit(password_label, (50, 135))

        login_surface = font.render(login_text, True, (255, 255, 255))
        password_surface = font.render('*' * len(password_text), True, (255, 255, 255))
        screen.blit(login_surface, (input_rect_login.x + 5, input_rect_login.y + 5))
        screen.blit(password_surface, (input_rect_password.x + 5, input_rect_password.y + 5))

        pygame.draw.rect(screen, (255, 255, 255), input_rect_login, 2 if active_login else 1)
        pygame.draw.rect(screen, (255, 255, 255), input_rect_password, 2 if active_password else 1)

        # Кнопки входа и регистрации
        register_label = font.render("Регистрация", True, (255, 255, 255))
        login_label = font.render("Вход", True, (255, 255, 255))
        screen.blit(register_label, (register_button.x + 10, register_button.y + 5))
        screen.blit(login_label, (login_button.x + 15, login_button.y + 5))

        if error_message:
            error_surface = error_font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (100, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect_login.collidepoint(event.pos):
                    active_login = True
                    active_password = False
                elif input_rect_password.collidepoint(event.pos):
                    active_login = False
                    active_password = True
                elif register_button.collidepoint(event.pos):
                    registration_screen()
                    return False
                elif login_button.collidepoint(event.pos):
                    users = load_users()
                    if login_text in users and users[login_text] == password_text:
                        return True
                    else:
                        error_message = "Неверный логин или пароль"

            if event.type == pygame.KEYDOWN:
                if active_login:
                    if event.key == pygame.K_BACKSPACE:
                        login_text = login_text[:-1]
                    else:
                        login_text += event.unicode

                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode

                if event.key == pygame.K_RETURN:
                    users = load_users()
                    if login_text in users and users[login_text] == password_text:
                        return True
                    else:
                        error_message = "Неверный логин или пароль"

        pygame.display.flip()
        clock.tick(30)

# Основной цикл
while True:
    if login_screen():
        print("Вход выполнен. Переход к игре...")
