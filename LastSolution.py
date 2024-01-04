import pygame
import sys
import random
import numpy as np
import time


pygame.init()

WIDTH, HEIGHT = 400, 400
CELL_SIZE = 100
AGENT_COLOR = (0, 255, 0)
TREASURE_COLOR = (255, 0, 0)
HOLE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)

treasure_position = [3, 3]

# Ініціалізація Q-таблиці (матриці для зберігання значень Q)
q_table = np.zeros((4, 4, 4))  

num_holes = 4
holes = []

for _ in range(num_holes):
    hole_x = random.randint(0, 3)
    hole_y = random.randint(0, 3)


    while (hole_x, hole_y) == (0, 0) or (hole_x, hole_y) == (3, 3):
        hole_x = random.randint(0, 3)
        hole_y = random.randint(0, 3)

    holes.append((hole_x, hole_y))


reward_for_treasure = 10
penalty_for_hole = -2
penalty_for_repeating_path = -1
cost_of_movement = 1
bonus_for_unvisited_cell = 1
penalty_for_visited_cell = 0

# Швидкість навчання та дисконтний фактор
learning_rate = 0.1
discount_factor = 0.9

# Ймовірність помилкового виконання дії
error_probability = 0.1

total_time_spent = 0
total_wins = 0
total_points = 0

max_attempts = 100
max_time = 1  # у сек

n = 50  

# Wbrk lkz snthfwsq
for iteration in range(n):
    # Початкові значення агента, пам'яті та очок
    agent_position = [0, 0]
    memory = []
    agent_points = 5

    total_attempts = 0
    iteration_start_time = time.time()

    # Цикл для гри
    while total_attempts < max_attempts and (time.time() - iteration_start_time) < max_time and agent_points >= cost_of_movement:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        total_attempts += 1
        start_time = time.time()

        # Вибір дії згідно Q-таблиці з можливою помилкою
        if random.uniform(0, 1) < error_probability:
            action = random.randint(0, 3)  # Випадкова дія при помилці
        else:
            action = np.argmax(q_table[tuple(agent_position)])

        new_position = agent_position.copy()
        if action == 0 and new_position[1] > 0:
            new_position[1] -= 1
        elif action == 1 and new_position[1] < 3:
            new_position[1] += 1
        elif action == 2 and new_position[0] > 0:
            new_position[0] -= 1
        elif action == 3 and new_position[0] < 3:
            new_position[0] += 1

       
        reward = 0
        if tuple(new_position) in holes:
            reward = penalty_for_hole
            new_position = [0, 0]
            memory = []  
        elif new_position == treasure_position:
            reward = reward_for_treasure
            print("Вітаємо! Ви знайшли скарб.")
            total_time_spent += time.time() - iteration_start_time
            average_time_per_attempt = total_time_spent / total_attempts
            total_wins += 1
            total_points += agent_points
            break  

        if new_position in memory:
            agent_points += penalty_for_visited_cell
            reward = penalty_for_repeating_path  
            new_position = agent_position.copy()
        else:
            if new_position not in memory:
                agent_points += bonus_for_unvisited_cell
            

        if agent_points <= 0:
            print("Гра завершилася поразкою. Агент втратив всі очки.")
            pygame.quit()
            sys.exit()

        # Додавання поточного стану в пам'ять
        memory.append(agent_position.copy())

        agent_points -= cost_of_movement

        # Оновлення Q-значення
        current_q_value = q_table[tuple(agent_position + [action])]
        max_future_q_value = np.max(q_table[tuple(new_position)])
        new_q_value = (1 - learning_rate) * current_q_value + learning_rate * (reward + discount_factor * max_future_q_value)
        q_table[tuple(agent_position + [action])] = new_q_value

        end_time = time.time()
        total_time_spent += end_time - start_time

        # Очистка екрану
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(BG_COLOR)

        pygame.draw.rect(screen, AGENT_COLOR, (agent_position[0] * CELL_SIZE, agent_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, TREASURE_COLOR, (treasure_position[0] * CELL_SIZE, treasure_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for hole in holes:
            pygame.draw.rect(screen, HOLE_COLOR, (hole[0] * CELL_SIZE, hole[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Оновлення вікна
        pygame.display.flip()

        pygame.time.delay(10)

        # Оновлення позиції агента
        agent_position = new_position.copy()

if total_wins == 0:
    print("Агент не знайшов скарб в жодній ітерації.")
else:
    average_points = total_points / n
    average_time_spent = total_time_spent / n
    win_percentage = (total_wins / n) * 100

    print("")
    print(f"Середня кількість очок: {average_points}")
    print(f"Середній час пошуку рішення: {average_time_spent} секунд")
    print(f"Відсоток перемог: {win_percentage}%")

pygame.quit()
sys.exit()
