import pygame, sys
# v 1.0a (newest)

def renderText(surf, size, pos, color, text, width=240, text_type="sys", shadow=False, shadow_amp=1, shadow_color=(150, 150, 150), centered=False, bubble=False, bubble_color=(0, 0, 0), right=False, dot=True, bubble_amp=1):
    txt_size = [0, 0]
    if text_type == "sys":
        fnt = pygame.font.Font("data/scripts/fonts/noTmeFontTitle.ttf", size)
        off = 0
        txt = fnt.render(text, False, color)
        txt_size_rect = txt.get_rect()
        if centered:
            off = txt_size_rect.width/2
        if right:
            off = txt_size_rect.width
        if bubble:
            # bubble
            pos_bubble_off = txt_size_rect.height*(1-bubble_amp)/2
            pygame.draw.rect(surf, bubble_color, [pos[0]-off-round(size/4*bubble_amp), pos[1]-round(size/4*bubble_amp)+pos_bubble_off, round(txt_size_rect.width*bubble_amp)+2*round(size/4*bubble_amp), txt_size_rect.height*bubble_amp+2*round(size/4*bubble_amp)])
            pygame.draw.rect(surf, bubble_color, [pos[0]-off-2*round(size/4*bubble_amp), pos[1]+pos_bubble_off, round(size/4*bubble_amp), size*bubble_amp])
            pygame.draw.rect(surf, bubble_color, [pos[0]-off-round(size/4*bubble_amp)+round(txt_size_rect.width*bubble_amp)+2*round(size/4*bubble_amp), pos[1]+pos_bubble_off, round(size/4*bubble_amp), size*bubble_amp])
            # arrow
            if dot:
                pygame.draw.rect(surf, bubble_color, [pos[0]-0.5*round(size/4), pos[1]+txt_size_rect.height+2*round(size/4), round(size/4), round(size/4)])
            
        if shadow:
            txtsh = fnt.render(text, False, shadow_color)
            surf.blit(txtsh, (pos[0]+shadow_amp-off, pos[1]+shadow_amp))
        surf.blit(txt, (pos[0]-off, pos[1]))
    elif text_type == "pixel":
        txt = Text()
        if shadow:
            surf = txt.WriteText(size, text, pos[0]+size*shadow_amp, pos[1]+size*shadow_amp, width, surf, "blue")
        surf = txt.WriteText(size, text, pos[0], pos[1], width, surf)

    return surf

class Text():
    def __init__(self):
        # font 
        self.scaleF = 1
        self.CharacterOrder = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "-", ".", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/", "+", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.CharsRect = []
        for i in range(len(self.CharacterOrder)):
            if self.CharacterOrder[i] == " ":
                self.CharsRect.append([0, 7*self.scaleF])
                self.CharsRect.append([i*self.scaleF*5, 0])
            else:
                self.CharsRect.append([i*self.scaleF*5, 0])
            
        self.Fx = 0
        self.Fy = 0
        self.CharW = 5*self.scaleF
        self.CharH = 8*self.scaleF
        self.text = []
        self.textNum = [len(self.CharacterOrder)]
        self.textToNum = 0

        # font img
        self.font2 = pygame.image.load("data/scripts/fonts/fontWhite.png").convert_alpha()
        self.Font2 = self.font2.copy()
        self.font1 = pygame.image.load("data/scripts/fonts/fontBlue.png").convert_alpha()
        self.Font1 = self.font1.copy()
        
    def ResizeFont(self, newFontSize):
        self.scaleF = newFontSize
        
        self.CharsRect = []
        for i in range(len(self.CharacterOrder)):
            if self.CharacterOrder[i] == " ":
                self.CharsRect.append([0, 7*self.scaleF])
                self.CharsRect.append([i*self.scaleF*5, 0])
            else:
                self.CharsRect.append([i*self.scaleF*5, 0])
            
        self.CharW = 5*self.scaleF
        self.CharH = 8*self.scaleF
        self.Font2 = pygame.transform.scale(self.font2, (int(330*self.scaleF), int(8*self.scaleF)))
        self.Font1 = pygame.transform.scale(self.font1, (int(330*self.scaleF), int(8*self.scaleF)))
    
    def WriteText(self, fontSize, blitText, xText, yText, xMax, surf, colour="white"):
        self.ResizeFont(fontSize)
        
        xMax -= self.CharW
        self.text = list(blitText)
        for i in range(len(self.text)):
            self.textToNum = self.CharacterOrder.index(self.text[i])
            self.textNum.insert(-1, self.textToNum)
        self.Fx = xText
        self.Fy = yText
        for i in range(len(self.textNum)):
            if not self.textNum[i] == 28:
                if colour == "blue":
                    surf.blit(self.Font1, (self.Fx, self.Fy), [self.CharsRect[self.textNum[i]][0], self.CharsRect[self.textNum[i]][1], self.CharW, self.CharH])
                elif colour == "white":
                    surf.blit(self.Font2, (self.Fx, self.Fy), [self.CharsRect[self.textNum[i]][0], self.CharsRect[self.textNum[i]][1], self.CharW, self.CharH])
                self.Fx += self.CharW
            else:
                self.Fx += self.CharW 
                if self.Fx >= xMax-self.CharW*5:
                    self.Fy += self.CharH
                    self.Fx = xText
            if self.Fx >= xMax:
                self.Fy += self.CharH
                self.Fx = xText
        self.Fx = 0
        self.textToNum = 0
        self.textNum = [28]

        return surf
