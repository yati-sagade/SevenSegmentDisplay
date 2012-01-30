'''
Created on Jan 28, 2012

@author: yati
'''
import pygame
import sys
from sevensegment import *

pygame.init()


if __name__ == '__main__':
    #ssdchars = [SevenSegmentChar(k, width=10) for k in sorted(SSD_CHAR_MAP.keys()) if SSD_CHAR_MAP[k]]
    display = SevenSegmentDisplay(200, 50, 'hola Yati', colour=(0xcc, 0xcc, 0xcc), char_width=10)
    scr = pygame.display.set_mode((800,400))
    scr.fill((0,0,0))
    i = 0
    #-------------------------------------------------- for ssdchar in ssdchars:
        #------------ r = ssdchar.surface.get_rect().move((i * ssdchar.width,0))
        #------------------------------------------ scr.blit(ssdchar.surface, r)
        #----------------------------------------------------------------- i +=1
    scr.blit(display.surface, display.surface.get_rect())
    pygame.display.flip()
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                sys.exit()
    
    
    