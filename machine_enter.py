mem = bytearray([0] * (2 ** 10))
reg = [bytearray([0] * 4) for i in range(32)]

IR = bytearray([0] * 4)  # 当前指令
AR = bytearray([0] * 4)  # mem的地址缓存器
DR = bytearray([0] * 4)  # mem的数据缓存器

S = bytearray([0] * 4)  # ALU的S缓存器
T = bytearray([0] * 4)  # ALU的T缓存器

PC = bytearray([0] * 4)  # PC
AC = bytearray([0] * 4)  # AC
ZF = 0  # 零
SF = 0  # 符号
OF = 0  # 溢出

signal_control_in = {
    'DR-MM': 0,
    'DR': 0,
    'AR': 0,
    'IR': 0,
    'T': 0,
    'S': 0,
    'REG': 0,  # 1-32,0表示不响应
    'PC': 0,
}
signal_control_out = {
    'AR-MM': 0,
    'DR-MM': 0,
    'DR': 0,
    'T': 0,
    'S': 0,
    'REG': 0,  # 1-32,0表示不响应
    'PC': 0,
}

SBUS = [[], []]  # 输入态，输出态
MMBUS = [[], []]  # 输入态，输出态
ALU = [0, '', 0]  # [0]:1-32; [2]:一元运算的参数x，或者 立即数的数
PC_add = [0]

# 微命令 版本 未完善
# from BackEnd.Machine.Micro_control import *
# 微操作
from BackEnd.Machine.Micro_control_op import Micro_control_op, bin_dec
from BackEnd.Machine.Micro_control_op import op_plus, op_cover, op_xor, op_left


def update():
    global SBUS, MMBUS, signal_control_in, signal_control_out, ALU, PC_add, SF, OF, S, T, mem, DR, IR, AR, PC, AC, reg

    ZF_t=0

    if MMBUS[0]:
        for t_ in range(len(DR)):
            DR[t_] = mem[bin_dec(AR) + t_]
    for i in MMBUS[1]:
        if i == 'AR-MM':
            pass
        if i == 'DR-MM':
            for t_ in range(len(DR)):
                mem[bin_dec(AR) + t_] = DR[t_]

    if ALU[1]:
        if ALU[1] == '+':
            op_plus(T, S, reg[int(ALU[0]) - 1])
        elif ALU[1] == '^':
            op_xor(T, S, reg[int(ALU[0]) - 1])
        elif ALU[1] == '<<':
            op_cover(T, op_left(S, ALU[2]))
        elif ALU[1] == '+i':
            temp = bin_dec(S)
            if temp > 32768:
                temp = temp - (2 ** 16)
            else:
                temp = temp
            num = temp + ALU[2]
            if num < 0:
                num = (2 ** 16) + num
            else:
                num = num
            for i in range(len(T)):
                T[i] = num % 256
                num = num >> 8
        elif ALU[1] == '==':
            flag = 0
            for i in range(4):
                if reg[int(ALU[0]) - 1] != S:
                    flag = 1
            if flag == 0:
                ZF_t = 1
            else:
                ZF_t = 0

    if PC_add[0]:
        if PC_add[0] == 1:
            op_plus(PC, PC, bytearray([4, 0, 0, 0]))
        elif PC_add[0] != 1:
            op_plus(PC, PC, bytearray([0, 0, 0, 0]), PC_add[0])

    if len(SBUS[1]) != 1:
        pass
    else:
        for i in SBUS[0]:
            if i == 'DR':
                op_cover(DR, SBUS[1][0])
            elif i == 'AR':
                op_cover(AR, SBUS[1][0])
            elif i == 'IR':
                op_cover(IR, SBUS[1][0])
            elif i == 'T':
                op_cover(T, SBUS[1][0])
            elif i == 'S':
                op_cover(S, SBUS[1][0])
            elif i == 'PC':
                op_cover(PC, SBUS[1][0])
            elif 0 < int(i) < 33:  # 1-32,0表示不响应
                op_cover(reg[int(i) - 1], SBUS[1][0])

    if MMBUS[0]:
        for t_ in range(len(DR)):
            DR[t_] = mem[bin_dec(AR) + t_]
    for i in MMBUS[1]:
        if i == 'AR-MM':
            pass
        if i == 'DR-MM':
            for t_ in range(len(DR)):
                mem[bin_dec(AR) + t_] = DR[t_]

    return ZF_t


class Machine:

    def __init__(self, machine_instruct):
        self.__theMachine = machine_instruct
        # self.__Micro_control = Micro_control()
        self.__Micro_control_op = Micro_control_op()

    def run(self):
        global SBUS, MMBUS, signal_control_in, signal_control_out, ALU, PC_add, ZF, SF, OF, S, T
        print("开始执行了")
        t = 1
        while (1):
            print(str(format(t, '02o')) + "编码:", end="")
            t += 1
            for i in range(4):
                print(format(mem[bin_dec(PC) + 3 - i], '08b'), end="  ")
            print("")
            if mem[bin_dec(PC)] == 255:
                break

            # 微操作
            for T_machine in range(3):
                for T_clock in range(4):
                    SBUS = [[], []]  # 输入态，输出态
                    MMBUS = [[], []]  # 输入态，输出态
                    ALU = [0, '', 0]
                    PC_add = [0]

                    if self.__Micro_control_op.final():
                        ZF = 0  # 零
                        SF = 0  # 符号
                        OF = 0  # 溢出
                    else:
                        ZF, SF, ALU, SBUS, MMBUS = self.__Micro_control_op.run(T_machine, T_clock, PC_add, IR, ALU,
                                                                               SBUS, MMBUS, signal_control_in,
                                                                               signal_control_out, ZF, SF)
                        ZF = 0  # 零
                        SF = 0  # 符号
                        OF = 0  # 溢出
                        ZF=update()
                self.__Micro_control_op.final_reset()

            # 微命令 版本 未完善
            # for T_machine in range(3):
            #     for T_clock in range(4):
            #         SBUS = [[], []]  # 输入态，输出态
            #         MMBUS = [[], []]  # 输入态，输出态
            #         if self.__Micro_control.final():
            #             pass
            #         else:
            #             self.__Micro_control.run(IR, ALU, SBUS, MMBUS, signal_control_in, signal_control_out)
            #             update()
            #     self.__Micro_control.final_reset()
        # print(mem[bin_dec(PC):bin_dec(PC)+4])
        print("结束了")
        # print(signal_control_out)
        # print(signal_control_in)
        # print(SBUS)
        # print(MMBUS)
        # print("--------------------------")
        # for i in mem[1:5]:
        #     print(format(i, '08b'))
        # print(AR)
        # print(DR)
        # print(reg[31])
