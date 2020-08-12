# DVI example
This is the [nMigen](https://github.com/nmigen/nmigen) port of the [OLED VGA example](https://github.com/emard/ulx3s-misc/tree/master/examples/oled/proj/ulx3s_oled_vga_vhdl) for the [ULX3S FPGA board](https://ulx3s.github.io/). This example takes VGA style input (pixel clock, RGB pixel data, vsync, hsync, and blank) and displays it as video on an OLED screen.

To build this example, you need [Yosys](https://github.com/YosysHQ/yosys), [nextpnr](https://github.com/YosysHQ/nextpnr), [project Trellis](https://github.com/YosysHQ/prjtrellis), and [openFPGAloader](https://github.com/trabucayre/openFPGALoader) installed. Then simply execute:

```bash
python top_oled_vga.py <FPGA variant>
```

where `<FPGA variant>` is either `12F`, `25F`, `45F`, or `85F` depending on the size of the FPGA on your ULX3S board. I have an `85F` board so I run:

```bash
python top_oled_vga.py 85F
```
