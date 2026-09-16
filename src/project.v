/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_tom (
    input  wire [7:0] ui_in,    // Dedicated inputs: 8 encoder input lines
    output wire [7:0] uo_out,   // Dedicated outputs: [2:0] encoded value, [3] valid flag
    input  wire [7:0] uio_in,   // IOs: Input path (unused)
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  reg [2:0] encoded;
  reg       valid;

  // 8:3 Priority Encoder
  // Highest-index active input wins priority
  always @(*) begin
    if (ui_in[7])      begin encoded = 3'd7; valid = 1'b1; end
    else if (ui_in[6]) begin encoded = 3'd6; valid = 1'b1; end
    else if (ui_in[5]) begin encoded = 3'd5; valid = 1'b1; end
    else if (ui_in[4]) begin encoded = 3'd4; valid = 1'b1; end
    else if (ui_in[3]) begin encoded = 3'd3; valid = 1'b1; end
    else if (ui_in[2]) begin encoded = 3'd2; valid = 1'b1; end
    else if (ui_in[1]) begin encoded = 3'd1; valid = 1'b1; end
    else if (ui_in[0]) begin encoded = 3'd0; valid = 1'b1; end
    else                begin encoded = 3'd0; valid = 1'b0; end
  end

  // Output mapping: uo_out[2:0] = encoded value, uo_out[3] = valid flag, rest unused
  assign uo_out  = {4'b0000, valid, encoded};
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, uio_in, 1'b0};

endmodule
