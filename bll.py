"""
    游戏逻辑控制器，负责处理游戏核心算法．
    Business Logic Layer
"""
from model import Location
import random


class GameCoreController:
    def __init__(self):
        self.__list_merge = None
        self.__map = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.__list_empty_location = []
        self.score = 0

    @property
    def map(self):
        return self.__map

    def __zero_to_end(self):
        """
            零元素移动到末尾.
        """
        for i in range(-1, -len(self.__list_merge) - 1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)

    def __merge(self):
        """
            合并
        """
        self.__zero_to_end()

        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                self.__list_merge[i] += self.__list_merge[i + 1]
                del self.__list_merge[i + 1]
                self.__list_merge.append(0)
                # 这里self.__list_merge[i]已经是合并之后的那个了，直接加上。
                self.score += self.__list_merge[i]

    # def __move_left(self):
    def move_left(self):
        """
            向左移动
        """
        for line in self.__map:
            self.__list_merge = line
            self.__merge()

    # def __move_right(self):
    def move_right(self):
        """
            向右移动
        """
        for line in self.__map:
            self.__list_merge = line[::-1]
            self.__merge()
            line[::-1] = self.__list_merge

    # def __move_up(self):
    def move_up(self):
        self.__square_matrix_transpose()
        self.move_left()
        self.__square_matrix_transpose()

    # def __move_down(self):
    def move_down(self):
        self.__square_matrix_transpose()
        self.move_right()
        self.__square_matrix_transpose()

    def __square_matrix_transpose(self):
        """
            方阵转置
        :param sqr_matrix: 二维列表类型的方阵
        """
        for c in range(1, len(self.__map)):
            for r in range(c, len(self.__map)):
                self.__map[r][c - 1], self.__map[c - 1][r] = self.__map[c - 1][r], self.__map[r][c - 1]

    # def move(self, dir):
    #     """
    #         移动
    #     :param dir: 方向,DirectionModel类型
    #     :return:
    #     """
    #     if dir == DirectionModel.UP:
    #         self.__move_up()
    #     elif dir == DirectionModel.DOWN:
    #         self.__move_down()
    #     elif dir == DirectionModel.LEFT:
    #         self.__move_left()
    #     elif dir == DirectionModel.RIGHT:
    #         self.__move_right()
    """
    2. 在GameCoreController类中，定义产生随机数功能.
   需求:在空白的位置上
       可能是2(90%),也可能是4(10%).
       1 - 10  --> 随机数 是1的概率是10%
       1 --100  --> 1 <=随机数<=38 的概率是38%

    """
    # 我的思路1：一个列表9个2,1个4，随机抽
    # 我的思路2：random.randint 结果如果是1-90就2， 91-100就是4

    # 产生每一格数字的,并把数字放进格子中为0 的位置，一次放一个

    def generate_new_number(self):
        # 获取空白位置
        self.__get_empty_location()
        # 列表为空会报错，return终止加数的代码
        if len(self.__list_empty_location) == 0:
            return
        loc = random.choice(self.__list_empty_location)

        self.__map[loc.r_index][loc.c_index] = self.__create_random_num()
        # 填完数字以后，在记录空格的列表中删除这一项
        self.__list_empty_location.remove(loc)

    def __get_empty_location(self):
        # 避免每一次找空位置的时候都创建一个新的列表，把创建空列表写进init
        # 每一次寻找空位置前，先清空原列表
        self.__list_empty_location.clear()
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r])):
                if self.__map[r][c] == 0:
                    # 把行号列号用对象封装好，放进列表
                    # 直接修改了实例变量（可以看做全局变量），不需要return了。
                    self.__list_empty_location.append(Location(r,c))


    def __create_random_num(self):
        # 非等概率生成数字
        #   方法1
        return 4 if random.randint(1,10) == 1 else 2

        #   方法2
        # random.choice
        #   方法3：
        #   random.randint(0, 3) > 0 and 2 or 4

    """
    3. 在GameCoreController类中，定义判断游戏是否结束的方法.
        是否具有空位置
        横向竖向没有相同的元素
    """
    def is_game_over(self):
        """
        :return: True代表退出游戏， False代表不退出游戏
        """
        # 借助上面已经写好的代码，看有无空
        if len(self.__list_empty_location) > 0:
            return False
        # 0-1 1-2 2-3，
        # 看是否每一列有相同的元素：取第0行，0-1 1-2 2-3 逐列取数字，定位元素比较。后面依次取第1,2,3行
        # [0][0]->[0][1];[0][1]->[0][2];[0][2]->[0][3]
        # [1][0]->[1][1];[1][1]->[1][2];[1][2]->[1][3]
        # 看是否每一行有相同的元素：取第0列，0-1 1-2 2-3 逐行取数字，定位元素比较。后面依次取第1,2,3列
        # [0][0]->[1][0];[1][0]->[2][0];[2][0]->[3][0]
        # [0][1]->[1][1];[1][1]->[2][1];[2][1]->[3][1]

        # 两个对比的索引值在数值上正好是互换
        # r = 1 第二次循环：第三位：[1][2]->[1][3]     [2][1]->[3][1]
        #                          [r][c]->[r][c+1]   [c][r]->[c+1][r]
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r])-1):
                if self.__map[r][c] == self.__map[r][c+1] or self.__map[c][r] == self.__map[c+1][r]:
                    # 不结束
                    return False
        return True
if __name__ == "__main__":
    controller = GameCoreController()
