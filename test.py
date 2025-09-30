import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    # 1. 创建黑色覆盖层
    over = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(over, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    
    # 2. 设置透明度
    over.set_alpha(200)
    
    # 3. 创建Game Over文字
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    # 4. 加载哭泣的こうかとん图像
    kk_img = pg.image.load("fig/8.png") 
    kk_img = pg.transform.rotozoom(kk_img, 0, 1)
    
    # 左侧的こうかとん
    kk_rect_left = kk_img.get_rect()
    kk_rect_left.center = (text_rect.left - 100, HEIGHT//2)  
    
    # 右侧的こうかとん
    kk_rect_right = kk_img.get_rect()
    kk_rect_right.center = (text_rect.right + 100, HEIGHT//2)
    
    # 5. 绘制所有元素
    screen.blit(over, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(kk_img, kk_rect_left)
    screen.blit(kk_img, kk_rect_right)
    
    # 6. 更新显示并等待5秒
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    初始化炸弹图像列表和加速度列表
    
    返回:
        炸弹Surface列表和加速度列表的元组
    """
    bb_imgs = []  # 炸弹图像列表
    bb_accs = []  # 加速度列表
    
    # 创建10个不同大小的炸弹
    for r in range(1, 11):
        # 创建炸弹Surface，大小为20*r × 20*r
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))  # 设置黑色为透明色
        # 绘制圆形炸弹，半径为10*r
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    
    # 创建加速度列表 [1, 2, 3, ..., 10]
    bb_accs = [a for a in range(1, 11)]
    
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 初始化炸弹图像和加速度列表
    bb_imgs, bb_accs = init_bb_imgs()
    
    # 初始炸弹（使用第一个图像）
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    
    vx, vy = +5, +5  # 基础速度
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [0, 0])

        # 碰撞检测
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # 处理键盘输入
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items(): 
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        # 移动こうかとん并检查边界
        kk_rct.move_ip(sum_mv)
        yoko, tate = check_bound(kk_rct)
        if not yoko or not tate:
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)

        # 炸弹的移动 - 随时间扩大和加速
        # 根据时间选择炸弹大小和加速度
        acc_index = min(tmr // 100, 9)  # 每500帧提升一个等级，最大为9
        avx = vx * bb_accs[acc_index]   # 计算实际速度
        avy = vy * bb_accs[acc_index]
        bb_img = bb_imgs[acc_index]     # 选择对应大小的炸弹图像
        
        # 移动炸弹
        bb_rct.move_ip(avx, avy)
        
        # 检查炸弹边界
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1 
        if not tate:
            vy *= -1
            
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()