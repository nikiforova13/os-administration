"""Собирает готовый образ ОЗУ name-output.cod для эмулятора КР580ВМ80."""

from pathlib import Path


TEXT = "ОЛЯ ИЕВЛЕВА"

# Машинный код КР580ВМ80 (Intel 8080), загружаемый с адреса 0000H.
program = bytearray(
    [
        0x0E,
        0x01,  # 0000: MVI C,01H
        0x21,
        0x00,
        0x00,  # 0002: LXI H,NAME (адрес заполняется ниже)
        0x06,
        len(TEXT),  # 0005: MVI B,0BH
        0x79,  # 0007: MOV A,C
        0xD3,
        0x00,  # 0008: OUT 00H
        0x7E,  # 000A: MOV A,M
        0xD3,
        0x00,  # 000B: OUT 00H
        0x0C,  # 000D: INR C
        0x79,  # 000E: MOV A,C
        0xE6,
        0x7F,  # 000F: ANI 7FH
        0x4F,  # 0011: MOV C,A
        0x23,  # 0012: INX H
        0x05,  # 0013: DCR B
        0xC2,
        0x07,
        0x00,  # 0014: JNZ 0007H
        0xC3,
        0x02,
        0x00,  # 0017: JMP 0002H
    ]
)

encoded_text = TEXT.encode("cp866")
data_address = len(program)
program[3] = data_address & 0xFF
program[4] = data_address >> 8
image = program + encoded_text

assert data_address == 0x001A
assert encoded_text == bytes.fromhex("8E 8B 9F 20 88 85 82 8B 85 82 80")
assert encoded_text.decode("cp866") == TEXT

output = Path(__file__).with_name("name-output.cod")
output.write_bytes(image)
print(f"Создан {output.name}: {len(image)} байт, данные с {data_address:04X}H")
