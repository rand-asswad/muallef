# Documentation

The documentation is built with
[R Markdown](https://rmarkdown.rstudio.com/)/[Bookdown](https://bookdown.org/)
and hosted with [Github Pages](https://pages.github.com/).

R Markdown is an awesome tool that features:
- [knitr](https://yihui.org/knitr/): an **R** engine for embedding code chunks in Markdown files
  (with support for other languages like **Python**).
- [pandoc](https://pandoc.org/): a universal document convertor.

For more details, refer to [R Markdown: The Definitive Guide](https://bookdown.org/yihui/rmarkdown/) or [bookdown](https://bookdown.org/yihui/bookdown/).

## Installation

In your **R** console run the following code.

```r
install.packages('bookdown')

# For PDF output install TinyTeX
install.packages("tinytex")
tinytex::install_tinytex()
```

The python engine used in to generate the documentation is R Markdown's default:
[reticulate](https://rstudio.github.io/reticulate/) which can be installed
by running the following R command:

```r
install.packages('reticulate')
```


## Usage

The documentation has embeded python code that runs in the project's virtual environment
make sure to properly initialize the project virtual environment in the directory `venv`
since it is hardcoded in [`index.rmd`](index.rmd).

Once the virtual environment is initialized properly,
the documentation can be generated using the `make` command.

```sh

make pdf        # Generate book.pdf (via LaTeX)
make gitbook    # Generate index.html
make html       # Generate onepage.html
make reveal     # Generate presentation.html
```

Consult [`Makefile`](Makefile) for more options.

## Directory Content

```sh
docs/
├── book/                           # gitbook output dir
├── img/                            # image dir
├── include/                        # TeX and HTML options
├── parts/                          # markdown content
├── _bookdown.yml                   # bookmark options
├── _output.yml                     # RMD options
├── .redirect ~> book/index.html    # page redirect to gitbook home
├── book.pdf -> book/book.pdf       # link to PDF book
├── index.html -> .redirect         # link to page redirect
├── index.rmd                       # main RMD file
├── onepage.html                    # onepage HTML output
├── presentation.html               # revealjs presenation output
├── presentation.md                 # presentation MD file
├── ref.bib                         # bibliography file
├── Makefile
└── README.md
```