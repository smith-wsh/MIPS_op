from BackEnd.Machine.machine_enter import DR, PC, reg, T

CM = bytearray([0] * 4)


def op_cover(a, b):
    for i in range(len(b)):
        a[i] = b[i]


def op_plus(a, b, c, shamt=0):
    global OF
    OF = 0
    if shamt != 0:
        a[0] = b[0] + shamt * 4
        return 1
    for i in range(len(a)):
        temp = b[i] + c[i] + OF
        OF = 0
        if temp > 255:
            OF = 1
            a[i] = temp - 256
        else:
            a[i] = temp


def op_xor(a, b, c):
    for i in range(len(a)):
        a[i] = b[i] ^ c[i]


def op_left(a, shmt):
    num = bin_dec(a)
    num = num << shmt
    t = [0, 0, 0, 0]
    for i in range(len(a)):
        t[i] = num % 256
        num = num >> 8
    return bytearray(t)


def bin_dec(a):
    num = 0
    for i in range(len(a)):
        num = num + a[i] * (256 ** i)
    return num


def dec_bin0(a, num):
    for i in range(len(a)):
        a[i] = num % 256
        num = num >> 8


def IR_R(IR):
    IR_t = bytearray([IR[3], IR[2], IR[1], IR[0]])
    op = IR_t[0] >> 2
    rs = ((IR_t[0] % 4) << 3) + (IR_t[1] >> 5)
    rt = IR_t[1] % 32
    rd = IR_t[2] >> 3
    shamt = ((IR_t[2] % 8) << 2) + (IR_t[3] >> 6)
    reg_func = IR_t[3] % 64
    return op, rs, rt, rd, shamt, reg_func


def IR_I(IR):
    IR_t = bytearray([IR[3], IR[2], IR[1], IR[0]])
    op = IR_t[0] >> 2
    rs = ((IR_t[0] % 4) << 3) + (IR_t[1] >> 5)
    rt = IR_t[1] % 32
    imm = bin_dec(IR[0:2])
    return op, rs, rt, imm


def IR_J(IR):
    IR_t = bytearray([IR[3], IR[2], IR[1], IR[0]])
    op = IR_t[0] >> 2
    address = IR_t[0] % 4 << 24 + bin_dec(IR[0:3])
    return op, address


class Micro_control_op:
    def __init__(self):
        self.__ready = 0

    def run(self, T_machine, T_clock, PC_add, IR, ALU, SBUS, MMBUS, signal_control_in, signal_control_out, ZF, SF):
        # 第一步 模拟中断控制，更新uPC，uIR，uAR寄存器
        # 第二步 输出状态控制流。并进入准备态
        # 第三步 模拟中断控制，更新uPC，uIR，uAR寄存器

        if T_machine == 0:  # 取指令
            if T_clock == 0:
                SBUS[1].append(PC)  # 输出
                SBUS[0].append('AR')  # 输入
                MMBUS[1].append('AR-MM')  # 输出
                return ZF, SF, ALU, SBUS, MMBUS
            elif T_clock == 1:
                PC_add[0] = 1
                return ZF, SF, ALU, SBUS, MMBUS
            elif T_clock == 2:
                MMBUS[0].append('DR-MM')  # 输入
                SBUS[1].append(DR)  # 输出
                SBUS[0].append('IR')  # 输入
                self.__ready = 1
                return ZF, SF, ALU, SBUS, MMBUS
            elif T_clock == 3:
                pass
                return ZF, SF, ALU, SBUS, MMBUS

        op, rs, rt, rd, shamt, reg_func = IR_R(IR)
        if op == 0:  # R 型
            if reg_func == 32:  # add
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        SBUS[1].append(reg[rs - 1])  # 输出
                        SBUS[0].append('S')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        ALU[0] = rt
                        ALU[1] = '+'
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        SBUS[1].append(T)  # 输出
                        SBUS[0].append(str(rd))  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
            elif reg_func == 38:  # xor
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        SBUS[1].append(reg[rs - 1])  # 输出
                        SBUS[0].append('S')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        ALU[0] = rt
                        ALU[1] = '^'
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        SBUS[1].append(T)  # 输出
                        SBUS[0].append(str(rd))  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
            elif reg_func == 0:  # sll
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        SBUS[1].append(reg[rt - 1])  # 输出
                        SBUS[0].append('S')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        ALU[1] = '<<'
                        ALU[2] = shamt
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        SBUS[1].append(T)  # 输出
                        SBUS[0].append(str(rd))  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
        elif op < 4:  # J 型
            op, address = IR_J(IR)
            if op == 2:  # J
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        SBUS[1].append(IR[0:2])  # 输出
                        SBUS[0].append('T')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        SBUS[1].append(T)  # 输出
                        SBUS[0].append('PC')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
            elif op == 3:  # jal
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
        elif op > 3:  # I 型
            op, rs, rt, imm = IR_I(IR)
            if op == 8:  # addi
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        SBUS[1].append(reg[rs - 1])  # 输出
                        SBUS[0].append('S')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        ALU[1] = '+i'
                        if imm > 32768:
                            imm = imm - (2 ** 16)
                            SF = 1
                        else:
                            imm = imm
                        ALU[2] = imm
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        SBUS[1].append(T)  # 输出
                        SBUS[0].append(str(rt))  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
            elif op == 43:  # sw
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        SBUS[1].append(reg[rs - 1])  # 输出
                        SBUS[0].append('S')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        ALU[1] = '+i'
                        if imm > 32768:
                            imm = imm - (2 ** 16)
                            SF = 1
                        else:
                            imm = imm
                        ALU[2] = imm
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        SBUS[1].append(T)  # 输出
                        SBUS[0].append('AR')  # 输入
                        MMBUS[1].append('AR-MM')  # 输出
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        SBUS[1].append(reg[rt - 1])  # 输出
                        SBUS[0].append('DR')  # 输入
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        MMBUS[1].append('DR-MM')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
            elif op == 4:  # beq
                if T_machine == 1:  # 取op数
                    if T_clock == 0:
                        SBUS[1].append(reg[rs - 1])  # 输出
                        SBUS[0].append('S')  # 输入
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                elif T_machine == 2:  # 执行
                    if T_clock == 0:
                        ALU[0] = rt
                        ALU[1] = '=='
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 1:
                        if ZF == 0:
                            if imm > 32768:
                                imm = imm - (2 ** 16)
                                SF = 1
                            else:
                                imm = imm
                            PC_add[0] = imm
                        self.__ready = 1
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 2:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS
                    elif T_clock == 3:
                        pass
                        return ZF, SF, ALU, SBUS, MMBUS

        # 测试
        # signal_control_in['AR'] = 1
        # signal_control_out['AR'] = 1
        #
        # SBUS[0].append('AR')
        # SBUS[0].append('32')
        # SBUS[0].append('DR')
        # SBUS[1].append(bytearray([1, 0, 0, 0]))
        #
        # MMBUS[1].append('DR-MM')
        self.__ready = 1

    def final(self):
        return self.__ready

    def final_reset(self):
        self.__ready = 0
