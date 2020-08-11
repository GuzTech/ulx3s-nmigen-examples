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

# Extra information
You need to have [nmigen-boards](https://github.com/nmigen/nmigen-boards) installed, and add the GDPI pins to the list of resources. The easiest way to this (until the pull request is merged) is to use [this file](https://github.com/nmigen/nmigen-boards/blob/b95f5a11b3174ea0c9a7c8dfa7cb187c178b9034/nmigen_boards/ulx3s.py). Just replace the contents of your ulx3s.py file, or just copy & paste [these lines](https://github.com/nmigen/nmigen-boards/blob/b95f5a11b3174ea0c9a7c8dfa7cb187c178b9034/nmigen_boards/ulx3s.py#L107-L115) to your own file.
