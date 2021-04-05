# MUALLEF

Muallef (arabic: **مؤلف**, pronounced *Mou'allef*, means *Composer*) is a humble `python`
library for **Music Information Retrieval (MIR)** algorithms.

Muallef is an implementation of MIR algorithms I studied in my master's thesis.
I used this code to produce the results presented in my [thesis](rand-asswad.github.io/muallef).

## Installation

Initialize the python environment:

```sh
python3 -m venv venv
pip3 install -r requirements.txt
```

**Warning:** using another name for python's virtual environment (`venv`) would work for using the library,
it will however break the dependency in
[docs/main.rmd](docs/main.rmd#L33)
if you want to produce the documentation in using
[R Markdown](https://rmarkdown.rstudio.com/)/[Bookdown](https://bookdown.org/).