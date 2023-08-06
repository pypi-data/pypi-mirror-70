[![Travis (.com)](https://img.shields.io/travis/com/Anselmoo/bashcalc?logo=travis)](https://travis-ci.com/Anselmoo/bashcalc)
[![Codecov](https://img.shields.io/codecov/c/github/Anselmoo/bashcalc?logo=Codecov)](https://codecov.io/gh/Anselmoo/bashcalc)
[![CodeFactor](https://img.shields.io/codefactor/grade/github/Anselmoo/bashcalc?logo=codefactor)](https://www.codefactor.io/repository/github/anselmoo/bashcalc)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)
[![GitHub](https://img.shields.io/github/license/Anselmoo/bashcalc?logo=GitHub)](https://github.com/Anselmoo/bashcalc/blob/master/LICENSE)

# bashcalc

## Instant calculating from the terminal into the terminal

---

`bashcalc` is an instant command-line tool for calculating directly mathematical expression into the terminal.

It is designed for working on cluster-server, where numbers or expressions have to be calculated without starting a new application or blogging any terminal windows. Therefore it will just show the result and immediately close. For this purpose, it is a pure `python` based and does not require any additional packages.

The idea is to have a simplistic tool that can quickly plot the results to the screen with various options:

1. simple example

```bash
╰─ bashcalc 1230/2
>>> 615
```

2. advanced example

```bash
╰─ pipenv run bashcalc "2*exp(3+(2//3))"
>>> 40.1710738463753358473695698194205760955810546875
```

3. advanced example with rounded output

```bash
╰─ pipenv run bashcalc "2*exp(3+(2//3))" -r 5
>>> 40.17107
```

4. advanced example as scientific output

```bash
╰─ pipenv run bashcalc "2*exp(3+(2//3))" -s 5 -b
>>> 4.01711E+1
```

## Installation

---

`pip install bashcalc`

or

`pip install https://github.com/Anselmoo/bashcalc.git`

or

```bash
python setup.py install
```

## Options

---

```bash

╰─ pipenv run bashcalc -h
usage: bashcalc [-h] [-c COLOR] [-b] [-u] [-i] [-r ROUND] [-s SCIENCE] [-v]
                infile

copy or rename any file(s) to a hash-secured filename via terminal

positional arguments:
  infile                Write the mathematic expression like: "(2 + 4) * 3"

optional arguments:
  -h, --help            show this help message and exit
  -c COLOR, --color COLOR
                        define the color of the output. The following options
                        are available:default, black,
                        red, green, yellow,
                        blue, magenta, cyan,
                        lightgray, darkgray,
                        lightred, lightgreen,
                        lightyellow, lightblue,
                        lightmagenta, lightcyan,
                        white
  -b, --bold            Print results in bold mode
  -u, --underlined      Print results in underlined mode
  -i, --int             Result will be printed as intiger-value
  -r ROUND, --round ROUND
                        Result will be printed as rounded float-value for
                        given number of digits
  -s SCIENCE, --science SCIENCE
                        Result will be printed in scientific notation
  -v, --version         displays the current version of bashcalc
```

## Author

---

- [Anselm Hahn](https://github.com/Anselmoo)

## Contributions

---

I'm happy to accept how to improve batchplot; please forward your [issues](https://github.com/Anselmoo/bashcalc/issues) or [pull requests](https://github.com/Anselmoo/bashcalc/pulls).

Keep in mind that [pull requests](https://github.com/Anselmoo/bashcalc/pulls) have to pass TravisCI in combination with [flake8](https://github.com/PyCQA/flake8), [black](https://github.com/psf/black), and [pydocstyle](https://github.com/PyCQA/pydocstyle).

## License

---

The source code of `bashplot` is licensed under the [MIT license](https://github.com/Anselmoo/bashcalc/blob/master/LICENSE).
