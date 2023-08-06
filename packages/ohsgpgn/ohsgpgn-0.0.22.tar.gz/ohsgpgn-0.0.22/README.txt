===========
  ohsgpgn
===========

This ohsgpgn is simple good password generator in which the generated password includes at least one number,ascii,digit and special chars('!@$%^&*()+').With argument length of password can be set. If the argument is less than 4, the generated password length will be at least 4.

    #!/usr/bin/env python3

    import ohsgpgn

    ohsgpgn.genGoodpass(10)
