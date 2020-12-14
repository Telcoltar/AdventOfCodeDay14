from typing import TextIO, Iterator
from argparse import ArgumentParser, Namespace
import logging
import re

parser: ArgumentParser = ArgumentParser()
parser.add_argument("--log", default="info")

options: Namespace = parser.parse_args()

level = logging.DEBUG

if options.log.lower() == "info":
    level = logging.INFO

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    level=level)

logger: logging.Logger = logging.getLogger(__name__)


def get_input_data(file_name: str) -> list[tuple[str, int, str]]:
    f: TextIO = open(file_name)

    input_data: list[tuple[str, int, str]] = []

    for line in f.readlines():
        com, num = line.split("=")
        if com.strip() == "mask":
            input_data.append(("mask", -1, num.strip()))
        else:
            input_data.append(("mem", int(re.search(r"\[(\d+)]", com.strip()).group(1)), f"{int(num.strip()):036b}"))

    return input_data


def apply_mask(mask: str, num: str) -> int:
    masked_num: str = ""
    for bit_m, bit_n in zip(mask, num):
        if bit_m == "X":
            masked_num += bit_n
        else:
            masked_num += bit_m
    return int(masked_num, 2)


def apply_mem_mask(mask_str, mem_add: int) -> Iterator[int]:
    masked_mem_add: list[str] = [""]
    new_masked_mem: list[str]
    for bit_m, bit_n in zip(mask_str, f"{mem_add:036b}"):
        if bit_m == "0":
            for i, st in enumerate(masked_mem_add):
                masked_mem_add[i] = st + bit_n
        elif bit_m == "1":
            for i, st in enumerate(masked_mem_add):
                masked_mem_add[i] = st + "1"
        else:
            new_masked_mem =  []
            for st in masked_mem_add:
                new_masked_mem.append(st + "1")
                new_masked_mem.append(st + "0")
            masked_mem_add = new_masked_mem
    return map(int, masked_mem_add)


def solution_part_1(file_name: str) -> int:
    input_data = get_input_data(file_name)
    current_mask: str = ""
    mem: dict[int, int] = {}
    for data_p in input_data:
        logger.debug(data_p)
        if data_p[0] == "mask":
            current_mask = data_p[2]
            logger.debug(current_mask)
        else:
            logger.debug(f"{data_p[1]}, {apply_mask(current_mask, data_p[2])}")
            mem[data_p[1]] = apply_mask(current_mask, data_p[2])
            logger.debug(mem)
    return sum(mem.values())


def solution_part_2(file_name: str) -> int:
    input_data = get_input_data(file_name)
    current_mask: str = ""
    mem: dict[int, int] = {}
    for data_p in input_data:
        logger.debug(data_p)
        if data_p[0] == "mask":
            current_mask = data_p[2]
            logger.debug(current_mask)
        else:
            logger.debug(f"{data_p[1]}, {apply_mask(current_mask, data_p[2])}")
            for add in apply_mem_mask(current_mask, data_p[1]):
                mem[add] = int(data_p[2], 2)
            logger.debug(mem)
    return sum(mem.values())


if __name__ == '__main__':
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))