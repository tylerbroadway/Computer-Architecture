"""CPU functionality."""
import sys

SP = 7
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xF4
        self.pc = 0
        self.flag = 0b00000000

    def load(self):
        """Load a program into memory."""
        try:
            address = 0
            with open(sys.argv[1]) as file:
                for line in file:
                    split_file = line.split("#")
                    value = split_file[0].strip()
                    if value == "":
                        continue
                    try:
                        instruction = int(value, 2)
                    except ValueError:
                        print(f"Invalid number '{value}'")
                        sys.exit(2)

                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print("File not found.")
            sys.exit(2)

    def run(self):
        running = True

        while running:
            instruction = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.running = False
                self.pc += 1

            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.reg[reg_a] = self.reg[reg_a] * \
                    self.reg[reg_b]
                self.pc += 3

            elif instruction == PUSH:
                self.reg[SP] -= 1
                register_num = self.ram_read(self.pc + 1)
                value = self.reg[register_num]
                top_of_stack_addr = self.reg[SP]
                self.ram[top_of_stack_addr] = value
                self.pc += 2

            elif instruction == POP:
                register_num = self.ram_read(self.pc + 1)
                top_of_stack_addr = self.reg[SP]
                value = self.ram_read(top_of_stack_addr)
                self.reg[register_num] = value
                self.reg[SP] += 1
                self.pc += 2
            elif instruction == CMP:
                op_a = self.ram_read(self.pc + 1)
                op_b = self.ram_read(self.pc + 2)
                self.alu("CMP", op_a, op_b)
                self.pc += 3

            elif instruction == JMP:
                reg_num = self.ram_read(self.pc + 1)
                self.pc = self.reg[reg_num]

            elif instruction == JEQ:
                if self.flag == 0b00000001:
                    reg_num = self.ram_read(self.pc + 1)
                    self.pc = self.reg[reg_num]
                else:
                    self.pc += 2
            elif instruction == JNE:
                if self.flag != 0b00000001:
                    reg_num = self.ram_read(self.pc + 1)
                    self.pc = self.reg[reg_num]
                else:
                    self.pc += 2
            else:
                self.pc += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
