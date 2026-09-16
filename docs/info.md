## How it works

This project implements an 8:3 priority encoder. It takes 8 input lines (`ui_in[7:0]`) and outputs the binary index of the highest-priority active input.

If multiple inputs are active at the same time, the input with the highest bit index takes priority. For example, if both `ui_in[2]` and `ui_in[5]` are high, the encoder outputs `5`.

The output is packed as follows:
- `uo_out[2:0]`: the 3-bit encoded value (0–7)
- `uo_out[3]`: a valid flag, high whenever at least one input is active, low when all inputs are 0

## How to test

Apply an 8-bit value to `ui_in` representing which lines are active (a `1` means that input is asserted). After one clock cycle, check `uo_out`:
- Bits `[2:0]` show the binary index of the highest active input
- Bit `[3]` is `1` if any input was active, or `0` if `ui_in` was all zeros

Example: setting `ui_in = 0b00100100` (bits 2 and 5 active) should give `uo_out[2:0] = 5` and `uo_out[3] = 1`, since bit 5 has higher priority than bit 2.

## External hardware

None. This project only uses the dedicated input/output pins.
