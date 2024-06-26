# Glass to Glass Delay Measurement System

## Quick start
### Installation
- Create virtual environment: 
```
python3 -m venv venv
```
- Acivate virtual environment
  - **Windows:** 
  ```
  venv/Scripts/activate
  ```
  - **Linux:** 
  ```
  source venv/bin/activate
  ```

- Install package: 
```
pip install .
```


### Run
- Acivate virtual environment (see Installation)

- Run: 
```
G2GDelay
```
- For analyzes run:
```
G2GDelay-analyze
```

<br>
<br>
<br>
<br>

## Comprehensive guide


- The Arduino should already be loaded with the correct script. If, for any reason, that is not the case, the code for the arduino is situated in the folder [Arduino_code/latency_test](Arduino_code/latency_test/).
- It is recommended to use a virtual environment to install this tool

<br>
  
**Note:** The python script includes more arguments for configuration. 
For more information run the script with -h argument.
```shell
G2Gdelay -h
``` 



## Usage
1. Follow installation procedure in quick start. The system is tested on Linux and Windows using python version 3.10
2. Run the tool as described in the quick start.

\** Make sure that there is a significant contrast on the screen between when the led is on and when the led is off. 



<br>
<br>
<br>


## References


    @inproceedings{bachhuber2016system,
      title={A System for High Precision Glass-to-Glass Delay Measurements in Video Communication},
      author={Bachhuber, Christoph and Steinbach, Eckehard},
      booktitle={IEEE International Conference on Image Processing (ICIP)},
      pages={2132--2136},
      year={2016},
    }
