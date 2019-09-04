"""
2048 控制台界面
"""
from bll import GameCoreController
import os
import pygame
from pygame.locals import *
import sys


class GameConsoleView:
    def __init__(self):
        self.__controller = GameCoreController()
        self.__PIXEL = 150
        self.__SIZE = 4
        self.__SCORE_PIXEL = 100

    def main(self):
        self.__start()
        self.__update()

    # 开始游戏
    def __start(self):
        # 随机产生两个数字并插入空白
        self.__controller.generate_new_number()
        self.__controller.generate_new_number()
        # self.__draw_map()
        # 开始界面绘制
        self.__show_init()

    def __show_init(self):
        # 初始化pygame
        pygame.init()
        # pygame.display.set_mode,初始化一个窗口。写多少就创建多大的窗口，width和height中哪一个写的0，就按照系统窗口的长或宽来创建窗口
        self.screen = pygame.display.set_mode(
            (self.__PIXEL * self.__SIZE, self.__PIXEL * self.__SIZE + self.__SCORE_PIXEL))
        # 游戏界面左上角的文字
        pygame.display.set_caption("2048")
        # 把前面这个对象pygame.Surface((PIXEL, PIXEL))创建4次
        # pygame.Surface（）,pygame中用来代表image的对象
        self.block = [pygame.Surface((self.__PIXEL, self.__PIXEL)) for i in range(4)]
        # 设置2048每个方格的颜色
        self.block[0].fill((238, 228, 218))
        self.block[1].fill((237, 224, 200))
        self.block[2].fill((242, 177, 121))
        self.block[3].fill((205, 193, 180))
        # (0, 0, 0)是黑色，(255, 255, 255)是白色，
        # surface((width, height).显示的是score背景的那个浅棕色的部分的大小。
        self.score_block = pygame.Surface((self.__PIXEL * self.__SIZE, self.__SCORE_PIXEL))
        # 对于分数条区域填充颜色
        self.score_block.fill((250, 248, 239))
        # 设置字体：通过None访问内建默认字体，第二个参数为size-小过每个格子的大小PIXEL
        self.map_font = pygame.font.Font(None, int(self.__PIXEL * 2 / 3))
        self.score_font = pygame.font.Font(None, int(self.__SCORE_PIXEL * 2 / 3))
        self.clock = pygame.time.Clock()
        self.show()

    # 游戏不断随着操作刷新
    def __update(self):
        # 一直循环-刷新
        while not self.__controller.is_game_over():
            # 每次循环访问你的目前的事件，r如果点叉号会退出
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            # clock.tick()他会计算距离上一次调用这个程序过去的second，限制一秒钟调用程序的次数。
            self.clock.tick(12)
            # 判断玩家的输入，移动地图
            self.__move_map_by_keyboard()
            # self.__draw_map()
            self.show()
        # 游戏结束后界面保留的时间
        pygame.time.delay(3000)

    def show(self):
        for i in range(self.__SIZE):
            for j in range(self.__SIZE):
                # print(True and "Score: ")，输出Score:,逻辑运算符：and or 一旦整体为True，把非逻辑运算符的部分代表整体
                # 这个值如果是0，那就从self.block的第0个和1个的颜色块中挑一个作为区域颜色。反之从第2个和第三个中挑。
                self.screen.blit(
                    self.__controller.map[i][j] == 0 and self.block[(i + j) % 2] or self.block[2 + (i + j) % 2],
                    (self.__PIXEL * j, self.__PIXEL * i))

                # 数值显示
                if self.__controller.map[i][j] != 0:
                    # 制作图片
                    #   取出第i行j列的数字，str了，RGB设置颜色
                    #   pygame.font.Font().render()是在一个新的Surface对象上绘制文本。写True字体就没有锯齿。
                    map_text = self.map_font.render(str(self.__controller.map[i][j]), True, (38, 38, 38))
                    # 生成图片放置的坐标
                    text_rect = map_text.get_rect()
                    text_rect.center = (self.__PIXEL * j + self.__PIXEL / 2, self.__PIXEL * i + self.__PIXEL / 2)
                    # 图片显示
                    self.screen.blit(map_text, text_rect)
        # 分数条显示
        #   分数条放在（0,600）。图片和背景都是以左上角的点为原点，向下和向右为正方向。600分数条处正好和4*4的格子擦边。
        self.screen.blit(self.score_block, (0, self.__SIZE * self.__PIXEL))

        # 生成分数图片
        #   pygame.font.Font().render(text, antialias, color, background=None)
        #   print(False or"Score: ")结果是 Score。
        score_text = self.score_font.render(
            (self.__controller.is_game_over() and "Game over with score " or "Score: ") + str(
                self.__controller.score), True,(119, 110, 101))
        # 生成分数位置
        #   .get_rect()获取文字图片的length和width
        score_rect = score_text.get_rect()
        #   (300, 650)。向右向下为正方向。300保证了在屏幕横向中间。650保证在600-700分数条的中间。
        #   但是这个点的坐标是整个文字图的左上角那个点。不写.center会左上角的点在中心，图片偏了。
        #   写了以后pygame自动为我们寻找能够使得图片中心在你想要的位置的坐标并return出来。
        score_rect.center = (self.__PIXEL * self.__SIZE / 2, self.__PIXEL * self.__SIZE + self.__SCORE_PIXEL / 2)
        # 分数图片显示在指定位置
        self.screen.blit(score_text, score_rect)
        # 让我们绘制的东西显示在屏幕上
        pygame.display.update()

    def __move_map_by_keyboard(self):
        # 接收玩家操作
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w] or pressed_keys[K_UP]:
            self.__controller.move_up()
            # 产生随机数字，插入空白
            self.__controller.generate_new_number()
        elif pressed_keys[K_s] or pressed_keys[K_DOWN]:
            self.__controller.move_down()
            self.__controller.generate_new_number()
        elif pressed_keys[K_a] or pressed_keys[K_LEFT]:
            self.__controller.move_left()
            self.__controller.generate_new_number()
        elif pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            self.__controller.move_right()
            self.__controller.generate_new_number()
            # def __draw_map(self):
            #     # 目的：为了让每次绘制界面的时候覆盖原来的，而不是每次显示一个新的
            #     # 让python调用Windows的命令执行操作
            #     os.system("cls")
            #     for line in self.__controller.map:
            #         for item in line:
            #             print(item, end=' ')
            #         print()


if __name__ == "__main__":
    view = GameConsoleView()
    view.main()
