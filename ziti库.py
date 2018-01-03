#coding=utf-8

import os
import pygame

pygame.init()

text = u"815555"
font = pygame.font.Font(os.path.join("fonts", "simsun.ttc"), 14)
rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))

pygame.image.save(rtext, "t.jpg")

{'6': '1', '7': '0', '2': '6', '1': '.', '9': '2', '8': '4', '5': '3', '4': '7',
 '0': '9', '3': '5'}