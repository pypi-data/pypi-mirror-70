=======
passgen
=======


Cli password generator
----------------------
Generates a password consisting of selected characters and the specified length.

Usage
-----
::

  usage: passgen [-h] [-l] [-u] [-d] [-s] [-a] [-c CUSTOM] [-n LENGTH]

  Generates a password consisting of selected characters and the specified length.

  optional arguments:
    -h, --help            show this help message and exit
    -l, --lower           password should contain lowercase letters
    -u, --upper           password should contain uppercase letters
    -d, --digits          password should contain digits
    -s, --special         password should contain special characters
    -a, --all             password should contain all of the above character groups, i.e. lowercase letters, uppercase letters, digits and
                          special characters
    -c CUSTOM, --custom CUSTOM
                          password should contain only characters passed as argument value, e.g. "abcd"; if the custom option is selected,
                          other options regarding the password structure are not taken into account
    -n LENGTH, --length LENGTH
                          set password length


If you want to copy generated password to clipboard use::

  passgen -a | xclip -sel clip

Tests
-----
The project is using pytest. Tests are in package directory, named ``[module]_test.py``.


Contribiuting
-------------
Please report any suggestions, feature requests, bug reports, or annoyances to the GitLab `issue tracker <https://gitlab.com/marekkon/passgen/-/issues>`_.


Related projects
----------------
- `passgen <https://pypi.org/project/passgen/>`_ - mature project with extensive functionality.
