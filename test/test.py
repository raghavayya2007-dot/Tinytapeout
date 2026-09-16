# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test: no inputs active -> valid should be 0")
    dut.ui_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b0000_0000  # encoded=0, valid=0

    dut._log.info("Test: only bit 0 active -> encoded=0, valid=1")
    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b0000_1000  # valid=1, encoded=000

    dut._log.info("Test: bit 3 active -> encoded=3, valid=1")
    dut.ui_in.value = 0b00001000
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b0000_1011  # valid=1, encoded=011

    dut._log.info("Test: bits 2 and 5 active -> priority picks bit 5, encoded=5")
    dut.ui_in.value = 0b00100100
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b0000_1101  # valid=1, encoded=101

    dut._log.info("Test: highest bit 7 active along with others -> priority picks bit 7, encoded=7")
    dut.ui_in.value = 0b10000001
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b0000_1111  # valid=1, encoded=111

    dut._log.info("Test: all bits active -> priority still picks bit 7, encoded=7")
    dut.ui_in.value = 0b11111111
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b0000_1111  # valid=1, encoded=111

    dut._log.info("All priority encoder tests passed")
