import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # sets number of registers to 8
        self.pc = 0  # program counter
        self.ram = [0] * 256   #
        self.mul = 0b10100010
        self.add = 0b10100000
        self.prn = 0b01000111
        self.ldi = 0b10000010
        self.hlt = 0b00000001
        self.cmp = 0b10100111
        self.jmp = 0b01010100
        self.jeq = 0b01010101
        self.jne = 0b01010110
        self.eql = 0    # cmp flag for equal to
        self.les = 0    # cmp flag for less than
        self.grt = 0    # cmp flag for greater than

    def load(self, file_name):
        """Load a program into memory."""
        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    # split before #comment / convert to a number
                    # splitting and stripping which will be read as our command
                    command = line.split('#')[0].strip()
                    # ignore blank lines
                    if command == '':
                        continue
                    # convert value to integer
                    instruction = int(command, 2)
                    # store the integer value at the given address
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file not found")
            sys.exit()

    if len(sys.argv) < 2:
        print("Please pass in a second filename: ls8.py example/second_filename.py")
        sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            # Compare and set flag according to == / less than /greater than being true or false
            # using a bolean binary || 0 = false / 1 = true
            if self.reg[reg_a] == self.reg[reg_b]:
                self.eql = 1

            if self.reg[reg_a] > self.reg[reg_b]:
                self.grt = 1

            if self.reg[reg_a] < self.reg[reg_b]:
                self.les = 1

        else:
            raise Exception("Unsupported ALU operation")

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

    def ram_read(self, MAR):
        return self.reg[MAR]

    def ram_write(self, MDR, MAR):
        self.reg[MAR] = MDR

    def run(self):
        """Run the CPU."""
        running = True

        print("\nLooking for Sprint Challenge Answers")
        while running:
            command = self.ram[self.pc]

            if command == self.ldi:
                #  Write             value         to  Ram   at  Index
                self.ram_write(self.ram[self.pc + 2], self.ram[self.pc + 1])

            elif command == self.prn:
                value = self.ram_read(self.ram[self.pc + 1])
                print(
                    f"printed = {value}")

            elif command == self.hlt:
                print("Stopping")
                running = False

            elif command == self.cmp:
                self.alu("CMP", self.ram[self.pc + 1], self.ram[self.pc + 2])

            elif command == self.jmp:
                # Jump to - Set program counter to address stored in the given reg
                self.pc = self.reg[self.ram[self.pc + 1]]
                continue

            elif command == self.jeq:
                # if equal is set to true
                if self.eql == 1:
                    # Jump to - Set program counter to address stored in the given reg
                    self.pc = self.reg[self.ram[self.pc + 1]]
                    #
                    continue

            elif command == self.jne:
                # if equal is false
                if self.eql == 0:
                    # Jump to - Set program counter to address stored in the given reg
                    self.pc = self.reg[self.ram[self.pc + 1]]
                    continue

            else:
                raise Exception("Unsupported operation")

            self.pc += 1 + (command >> 6)
