
import pygame

import mglobals

def text_objects(msg, fontobj, color='black'):
    color = mglobals.color_map[color]
    text_surf = fontobj.render(msg, True, color)
    return text_surf, text_surf.get_rect()

def message_display(msg, x=mglobals.DISPLAY_W/2, y=mglobals.DISPLAY_H/2, clear_color=None,
                    color='black', fntsize='big', center_coord=True):
    if clear_color:
        mglobals.GD.fill(mglobals.color_map[clear_color])

    textfont = pygame.font.Font('freesansbold.ttf', mglobals.fontsize_map[fntsize])
    text_surf, text_rect = text_objects(msg, textfont, color)
    if center_coord:
        text_rect.center = (x, y)
    else:
        text_rect.x, text_rect.y = x, y
    mglobals.GD.blit(text_surf, text_rect)
    pygame.display.update()


def draw_board():
    mglobals.GD.blit(mglobals.BACK_IMG, (0, 0))

def clear_msg_info():
    mglobals.MSG_CLRSCR.fill(mglobals.color_map['white'])
    mglobals.GD.blit(mglobals.MSG_CLRSCR, (808, 770))



