import sys
import json


class UVM:
    def __init__(self):
        self.memory = [0] * 256  # Пример размера памяти
        self.stack = []

    def load_binary(self, file_input):
        with open(file_input, 'rb') as f:
            self.binary = f.read()

    def run(self):
        pc = 0  # счетчик команд
        while pc < len(self.binary):
            opcode = self.binary[pc]
            if opcode == 0x43:  # LOAD_CONST
                value = (self.binary[pc + 1] << 8) | self.binary[pc + 2]
                self.stack.append(value)
                pc += 3
            elif opcode == 0x58:  # READ_MEMORY
                address = (self.binary[pc + 1] << 24) | (self.binary[pc + 2] << 16) | \
                          (self.binary[pc + 3] << 8) | self.binary[pc + 4]
                if 0 <= address < len(self.memory):
                    self.stack.append(self.memory[address])
                else:
                    print(f"Error: Memory address {address} out of range.")
                    break
                pc += 5
            elif opcode == 0x96:  # WRITE_MEMORY
                offset = (self.binary[pc + 1] << 8) | self.binary[pc + 2]
                if 0 <= offset < len(self.memory) and self.stack:
                    value = self.stack.pop()
                    self.memory[offset] = value
                else:
                    print(f"Error: Write memory address {offset} out of range or stack empty.")
                    break
                pc += 3
            elif opcode == 0xEF:  # SHIFT_LEFT
                address = (self.binary[pc + 1] << 24) | (self.binary[pc + 2] << 16) | \
                          (self.binary[pc + 3] << 8) | self.binary[pc + 4]
                if 0 <= address < len(self.memory):
                    value = self.memory[address]
                    shifted_value = value << 1  # Пример сдвига
                    self.stack.append(shifted_value)
                else:
                    print(f"Error: Memory address {address} out of range.")
                    break
                pc += 5
            else:
                print(f"Unknown opcode {opcode} at pc={pc}")
                break


def main(file_input, result_range):
    uvm = UVM()
    uvm.load_binary(file_input)
    uvm.run()

    # Сохранение результатов в JSON
    result = {
        "memory": uvm.memory[:int(result_range)],
        "stack": uvm.stack
    }

    with open("result.json", 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    input_file = sys.argv[1]
    result_range = int(sys.argv[2])
    main(input_file, result_range)
