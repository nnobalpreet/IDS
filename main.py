import sys
import os

input_str="python newscript.py ";

for i in range(1,len(sys.argv)):
    if(sys.argv[i]=="New_Container"):
       if(input_str <> "python newscript.py "):
          os.sys(input_str);
    else:
        input_str=input_str+sys.argv[i]+" ";
    print input_str;

