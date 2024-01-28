import pygame

from User.UserDao import UserDao


class Statistic:
    def __init__(self, display_position, player_list):
        self.display_position = display_position
        self.player_list = player_list
        self.user_dao = UserDao()

    def render_score(self, screen):
        font = pygame.font.Font(None, 36)
        message_text = font.render("Score:", True, (0, 0, 0))
        message_rect = message_text.get_rect(center=self.display_position)
        screen.blit(message_text, message_rect)
        display_position = self.display_position[1]

        for player in self.player_list:
            score_text = font.render(f"{player.player_name}: {self.get_score(player)}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(self.display_position[0], display_position + 30))
            display_position += 30
            screen.blit(score_text, score_rect)

    def get_score(self, player):
        score = 0
        points = self.user_dao.get_user_points(player.player_id)
        for points in points:
            score += points.value
        return score


    def get_leader(self):
        leader = self.player_list[0]
        for player in self.player_list:
            if self.get_score(player) > self.get_score(leader):
                leader = player
        return leader.player_name