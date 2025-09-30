import os
import random
import sys
import time
import math
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT :(-5,0),
    pg.K_RIGHT :(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    yoko,tate =True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate
def gameover(screen: pg.Surface) -> None:
    """
    游戏结束画面显示函数
    
    参数:
        screen: 主画面Surface
    """
    # 1. 创建用于绘制黑色矩形的空Surface
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    
    # 2. 设置Surface的透明度（半透明）
    overlay.set_alpha(200)
    
    # 3. 创建Game Over文本
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    
    # 4. 加载哭泣的こうかとん图像
    kk_img = pg.image.load("fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    
    # 5. 绘制
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(kk_img, kk_rect)
    
    # 6. 更新显示并等待
    pg.display.update()
    time.sleep(5)



#def gameover(screen: pg.Surface) -> None:
    over = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(over, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    over.set_alpha(200)
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    kk_img = pg.image.load("fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    screen.blit(over, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(kk_img, kk_rect)
    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200


    bb_img = pg.Surface((20,20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img,(255, 0, 0),(10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centerx = random.randint(0, HEIGHT)
    vx,vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items(): 
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        yoko, tate = check_bound(kk_rct)
        if not yoko or not tate:
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1 
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):
            return
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
