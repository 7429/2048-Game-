"""
    数据模型
        用于封装数据，使得代码阅读者知道数据背后的意义。
"""
class Location:
    """
        位置
    """
    def __init__(self,r,c):
        self.r_index = r
        self.c_index = c
