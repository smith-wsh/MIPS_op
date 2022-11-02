CM = bytearray([0] * 4)


def op_cover(a, b):
    for i in range(len(a)):
        a[i] = b[i]


def op_plus(a, b, c):
    global OF
    OF = 0
    for i in range(len(a)):
        temp = b[i] + c[i] + OF
        OF = 0
        if temp > 255:
            OF = 1
            a[i] = temp - 256
        else:
            a[i] = temp


def bin_dec(a):
    num = 0
    for i in range(len(a)):
        num = num + a[i] * (256 ** i)
    return num


def dec_bin0(a, num):
    for i in range(len(a)):
        a[i] = num % 256
        num = num >> 8


def mult_collect(K_flag, IR, uIR):
    a = bytearray([0] * 4)
    if K_flag:
        for i in range(len(a)):
            a[i] = IR[i]
    else:
        for i in range(len(a)):
            a[i] = uIR[i]
    return a


class Micro_control:
    def __init__(self):
        self.__ready = 0
        self.uPC = bytearray([0] * 4)
        self.uIR = bytearray([0] * 4)
        self.K_flag = 1

    def run(self, IR, ALU, SBUS, MMBUS, signal_control_in, signal_control_out):
        # 第一步 模拟中断控制，更新uPC，uIR，uAR寄存器
        # 第二步 输出状态控制流。并进入准备态
        # 第三步 模拟中断控制，更新uPC，uIR，uAR寄存器

        self.uAR = mult_collect(self.K_flag, IR, self.uIR)

        instruct = CM[bin_dec(self.uAR)]

        self.uIR = instruct[0]
        signal_control_in['AR'] = 1
        signal_control_out['AR'] = 1

        SBUS[0].append('AR')
        SBUS[0].append('32')
        SBUS[0].append('DR')
        SBUS[1].append(bytearray([1, 0, 0, 0]))

        MMBUS[1].append('DR-MM')
        self.__ready = 1

    def final(self):
        return self.__ready

    def final_reset(self):
        self.__ready = 0

    def K_start(self):
        return self.K_flag

    def K_start_reset(self):
        self.K_flag = 1
