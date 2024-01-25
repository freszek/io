
import pygame

import mglobals

def text_objects(msg, fontobj, color='black'):
    color = mglobals.color_map[color]
    text_surf = fontobj.render(msg, True, color)
    return text_surf, text_surf.get_rect()

def draw_board():
    mglobals.GD.fill((255, 255, 255))
    mglobals.GD.blit(mglobals.BACK_IMG, (0, 0))

def clear_msg_info():
    mglobals.MSG_CLRSCR.fill(mglobals.color_map['white'])
    mglobals.GD.blit(mglobals.MSG_CLRSCR, (808, 770))



