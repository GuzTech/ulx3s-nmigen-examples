# ULX3S nMigen examples
This repository contains [nMigen](https://github.com/nmigen/nmigen)) examples for the [ULX3S FPGA board](https://ulx3s.github.io/). You need to have [Yosys](https://github.com/YosysHQ/yosys), [nextpnr](https://github.com/YosysHQ/nextpnr), [project Trellis](https://github.com/YosysHQ/prjtrellis), and [openFPGAloader](https://github.com/trabucayre/openFPGALoader) installed.

Each directory contains an example, which you can build and run by simply running:

```bash
python top_<example>.py <FPGA variant>
```

where `<FPGA variant>` is either `12F`, `25F`, `45F`, or `85F` depending on the size of the FPGA on your ULX3S board. I have an `85F` board so to build the `dvi` example, I run:

```bash
python top_vgatest.py 85F
```

in the `dvi` folder.