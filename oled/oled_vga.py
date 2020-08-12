from nmigen import *
from nmigen.build import Platform
from nmigen_boards.ulx3s import *

from oled_init import *


class OLED_VGA(Elaboratable):
    def __init__(self, color_bits=8):
        self.i_clk_en = Signal()
        self.i_clk_pixel_ena = Signal()
        self.i_hsync = Signal()
        self.i_vsync = Signal()
        self.i_blank = Signal()
        self.i_pixel = Signal(color_bits)
        self.o_spi_resn = Signal(reset=1)
        self.o_spi_clk = Signal(reset=1)
        self.o_spi_csn = Signal(reset=1)
        self.o_spi_dc = Signal(reset=1)
        self.o_spi_mosi = Signal(reset=1)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        # Constants
        C_last_init_send_as_data = C(1, 16)

        # Internal signals
        R_reset_cnt = Signal(2, reset=0)
        # Initialization sequence replay counter.
        R_init_cnt = Signal(16, reset=0)
        # (15 downto 4) -- byte address of the config sequence
        # ( 3 downto 1) -- bit address 8 bits of each byte
        # (0)           -- spi clock cycle
        R_spi_data = Signal(8)
        R_dc       = Signal(reset=0) # 0 = command, 1 = data
        R_x        = Signal(7, reset=1)
        R_y        = Signal(6, reset=1)
        R_x_in     = Signal(7)
        R_y_in     = Signal(6)
        R_scanline = Array(Signal(8) for _ in range(96))

        # Track signal's pixel coordinates and buffer one line.
        with m.If(self.i_clk_pixel_ena):
            with m.If(self.i_vsync):
                m.d.sync += R_y_in.eq(0)
            with m.Else():
                with m.If(self.i_hsync):
                    m.d.sync += R_x_in.eq(0)
                with m.Else():
                    with m.If(self.i_blank == 0):
                        m.d.sync += R_scanline[R_x_in].eq(self.i_pixel)

                        # If R_x_in == 95
                        with m.If(R_x_in == 0b101_1111):
                            m.d.sync += R_x_in.eq(0)
                            m.d.sync += R_y_in.eq(R_y_in + 1)
                        with m.Else():
                            m.d.sync += R_x_in.eq(R_x_in + 1)

        with m.If(R_reset_cnt[-2:] != 0b10):
            m.d.sync += R_reset_cnt.eq(R_reset_cnt + 1)
        with m.Elif(R_init_cnt[4:] != len(oled_init_seq)):
            # Load new byte (either from init sequence or next pixel).
            with m.If(R_init_cnt[:4] == 0):
                with m.If(R_y_in == R_y):
                    m.d.sync += R_init_cnt.eq(R_init_cnt + 1)
                    with m.If(R_dc == 0):
                        # Init sequence.
                        m.d.sync += R_spi_data.eq(oled_init_seq[R_init_cnt[4:]])
                    with m.Else():
                        m.d.sync += R_spi_data.eq(R_scanline[R_x])
                        # Tracks XY pixel coordinates currently written to SPI display.
                        with m.If(R_x == 0b101_1111): # If R_x = 95
                            m.d.sync += R_x.eq(0)
                            m.d.sync += R_y.eq(R_y + 1)
                        with m.Else():
                            m.d.sync += R_x.eq(R_x + 1)
            with m.Else():
                with m.If(self.i_clk_en == 1):
                    m.d.sync += R_init_cnt.eq(R_init_cnt + 1)
                    with m.If(R_init_cnt[0] == 0): # Shift one bit to the right.
                        m.d.sync += R_spi_data.eq(Cat(0b0, R_spi_data[:-1]))

        # Send last N bytes as data.
        with m.If(R_init_cnt[4:] == ((len(oled_init_seq) - 1) - (C_last_init_send_as_data - 1))):
            m.d.sync += R_dc.eq(1)
        with m.If(R_init_cnt[4:] == (len(oled_init_seq) - 1)):
            m.d.sync += R_init_cnt[4:].eq((len(oled_init_seq) - 1) - (C_last_init_send_as_data - 1))

        m.d.comb += [
            self.o_spi_resn.eq(~R_reset_cnt[-2]),
            self.o_spi_csn .eq(R_reset_cnt[-2]), # CS = inverted reset
            self.o_spi_dc  .eq(R_dc),
            self.o_spi_clk .eq(~R_init_cnt[0]), # Counter LSB always to clock
            self.o_spi_mosi.eq(R_spi_data[-1])
        ]

        return m
