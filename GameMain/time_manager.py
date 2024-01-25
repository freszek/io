from datetime import datetime, timedelta
import pygame

class TimeManager:
    def __init__(self, start_time_str, display_position):
        self.round_start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        self.display_position = display_position

    def get_time_left(self):
        current_time = datetime.now()
        time_since_start = current_time - self.round_start_time
        time_left = timedelta(days=1) - time_since_start
        return time_left

    def render_time(self, screen):
        font = pygame.font.Font(None, 36)
        message_text = font.render("Time to end round:", True, (0, 0, 0))
        message_rect = message_text.get_rect(center=self.display_position)
        screen.blit(message_text, message_rect)

        time_left = self.get_time_left()
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_text = font.render(f"{hours:02}:{minutes:02}:{seconds:02}", True, (0, 0, 0))
        time_rect = time_text.get_rect(center=(self.display_position[0], self.display_position[1] + 30))

        screen.fill((255, 255, 255), time_rect)
        screen.blit(time_text, time_rect)

    def update_round(self, new_start_time_str):
        self.round_start_time = datetime.strptime(new_start_time_str, "%Y-%m-%d %H:%M:%S")

    def render_round_info(self, screen, round_number):
        font = pygame.font.Font(None, 36)
        round_text = font.render(f"Round: {round_number}/14", True, (0, 0, 0))
        round_rect = round_text.get_rect(center=(self.display_position[0], self.display_position[1] + 200))

        screen.fill((255, 255, 255), round_rect)
        screen.blit(round_text, round_rect)