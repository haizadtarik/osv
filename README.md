# Optimal surface voting for U-Net output

This repository contains code to apply optimal surface voting to the output of a FaultSeg/U-Net model to enhance faults detection

## Run

1. Build the Docker image: `docker build -t osv_unet .`
2. Run the Docker container: `docker run -v <DATA_FOLDER_PATH>:/app/data osv_unet`

    The data folder should contain the following structure and files:
    ```
    <DATA_FOLDER_PATH>
      |-- xs.dat # seismic input data
      |-- ep.dat # unet output with faults
    ```

    Ensure that ep.dat is the output of the Unet model before sigmoid activation function is applied

Reference:
1. [OSV](https://github.com/xinwucwp/osv) by Xinming Wu and Sergey Fomel