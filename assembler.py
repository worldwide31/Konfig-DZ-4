import sys
import json

# Команды УВМ
COMMANDS = {
    'LOAD_CONST': (0x43, 3),
    'READ_MEMORY': (0x58, 4),
    'WRITE_MEMORY': (0x96, 3),
    'SHIFT_LEFT': (0xEF, 4),
}


def assemble_instruction(command, operand):
    if command not in COMMANDS:
        raise ValueError(f"Unknown command: {command}")

    command_code, size = COMMANDS[command]
    if size == 3:
        return bytearray([command_code, (operand >> 8) & 0xFF, operand & 0xFF])
    else:
        return bytearray([command_code, (operand >> 24) & 0xFF, (operand >> 16) & 0xFF,
                          (operand >> 8) & 0xFF, operand & 0xFF])


def assemble(file_input, file_output, log_file):
    # Чтение исходного файла
    with open(file_input, 'r') as f:
        lines = f.readlines()

    binary_instructions = bytearray()
    log_entries = {}

    for line in lines:
        parts = line.strip().split()
        command = parts[0]
        operand = int(parts[1]) if len(parts) > 1 else 0

        binary_instruction = assemble_instruction(command, operand)
        binary_instructions.extend(binary_instruction)
        log_entries[command] = operand

    # Запись бинарного файла
    with open(file_output, 'wb') as f:
        f.write(binary_instructions)

    # Запись лог файла
    with open(log_file, 'w') as f:
        json.dump(log_entries, f, indent=4)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
