===========
  ohsgpgn
===========

This ohsgpgn is a simple good password generator. The generated password includes at least one number,one ascii,one capatalized ascii and one special chars('!@$%^&*()+').With argument, length of password can be set. If the argument(n) is  less than 10(n < 10), the generated password length will be at least 10.

    #!/usr/bin/env python3

    from ohsgpgn import ohsgpgn
  
    print(ohsgpgn.genGoodpass(20))


    oyj@shell_prompt$ python3 pass.py 
   
    zB!2X3!d*V#V!EwOnEK6



    #Using python shell(example)

    Python 3.6.9 (default, Apr 18 2020, 01:56:04) 

    [GCC 8.4.0] on linux

    Type "help", "copyright", "credits" or "license" for more information.

    >>> from ohsgpgn import *
    >>> ohsgpgn.genGoodpass(3)
    '&92DLE1Kf&'
    >>> ohsgpgn.genGoodpass(20)
    'ae5s67NN4H04bJt$Aajd'
    >>> ohsgpgn.genGoodpass(100)
    'IN5SATQaVW8E9JL)Q5K2oIJ02Ep5@YVMQ6CAY6LAXPIKDu*COCKGC0Y8EM2Q1VSCEE286XZT2Q8yMDX9JH8OYRXB7YHUPO0D2IDZ'
