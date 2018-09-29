# HEC-RAS-Python

Calling HEC-RAS from python 3.x 
## Acknowlegement of source
This work originates from the material provided by Tomasz Dysarz, in Poland. 

## How to use
HEC-RAS is free but not open source. I wish it was! That may have allowed me to create a much more integrated interface to the model from Python. As it is, the only way it allows to communicate is via the [Component Object Model](https://en.wikipedia.org/wiki/Component_Object_Model) of windows operating system. (Needless to say the solution is platform bound!). 

Following steps are necessary to get HEC-RAS-Python examples to run. 
1. Install [pywin32](https://pypi.org/project/pywin32/): 
```
pip install pywin32
```
2. Run makepy utility. Run the following in the command line
```
python c:\Python37\Lib\site-packages\win32com\client\makepy.py 
```
Note: ```c:\Python37\``` above, is only an example, replace it with the path of your own python installation. 

There will be a pop-up window. Select HECRAS River Analysis System (1.1) from the pop-up window and press OK. This will build definitions and import modules of RAS-Controller for use. You will see an output similar to the following
```
Generating to C:\Users\xxx\AppData\Local\Temp\gen_py\3.7\00020813-0000-0000-C000-000000000046x0x1x8.py
Building definitions from type library...
Generating...
Importing module
```

Now you are ready!


