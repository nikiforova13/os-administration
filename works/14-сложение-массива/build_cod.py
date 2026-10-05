"""Собирает образ ОЗУ array-sum.cod для практической работы № 14."""

from pathlib import Path


DATA_ADDRESS = 0x0100
RESULT_ADDRESS = 0x0120
VALUES = bytes([0xA1, 0x9B, 0xF0, 0x80, 0x40])

# Машинный код КР580ВМ80А (Intel 8080), загружаемый с адреса 0000H.
program = bytes(
    [
        0x21,
        0x00,
        0x01,  # 0000: LXI H,0100H
        0x06,
        len(VALUES),  # 0003: MVI B,05H
        0xAF,  # 0005: XRA A
        0x4F,  # 0006: MOV C,A
        0x86,  # 0007: ADD M
        0xD2,
        0x0C,
        0x00,  # 0008: JNC 000CH
        0x0C,  # 000B: INR C
        0x23,  # 000C: INX H
        0x05,  # 000D: DCR B
        0xC2,
        0x07,
        0x00,  # 000E: JNZ 0007H
        0x21,
        0x20,
        0x01,  # 0011: LXI H,0120H
        0x77,  # 0014: MOV M,A
        0x23,  # 0015: INX H
        0x79,  # 0016: MOV A,C
        0x77,  # 0017: MOV M,A
        0x76,  # 0018: HLT
    ]
)

image = bytearray(RESULT_ADDRESS + 2)
image[: len(program)] = program
image[DATA_ADDRESS : DATA_ADDRESS + len(VALUES)] = VALUES

expected_sum = sum(VALUES)
low = 0
high = 0
for value in VALUES:
    partial_sum = low + value
    low = partial_sum & 0xFF
    if partial_sum > 0xFF:
        high += 1

assert len(program) == 0x19
assert expected_sum == 0x02EC
assert (high << 8) | low == expected_sum
assert image[RESULT_ADDRESS : RESULT_ADDRESS + 2] == b"\x00\x00"

output = Path(__file__).with_name("array-sum.cod")
output.write_bytes(image)
print(
    f"Создан {output.name}: {len(image)} байт; "
    f"ожидаемый результат {high:02X}{low:02X}H"
)
