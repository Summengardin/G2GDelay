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

- Delete temp files
You can safely delete temporary directories created during installation: 
`build` and `*.egg-info`


- Run: 
```
G2GDelay
```
- For analyzes run:
```
G2GDelay-analyze
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


## Additional info


- The Arduino should already be loaded with the correct script. If, for any reason, that is not the case, the code for the arduino is situated in the folder [Arduino_code/latency_test](Arduino_code/latency_test/).
- It is recommended to use a virtual environment to install this tool
- Make sure that there is a significant contrast on the screen between when the led is on and when the led is off. 

<br>
  
**Note:** The python script includes more arguments for configuration. 
For more information run the script with -h argument.
```shell
G2Gdelay -h
``` 


<br>



## References


    @inproceedings{bachhuber2016system,
      title={A System for High Precision Glass-to-Glass Delay Measurements in Video Communication},
      author={Bachhuber, Christoph and Steinbach, Eckehard},
      booktitle={IEEE International Conference on Image Processing (ICIP)},
      pages={2132--2136},
      year={2016},
    }
