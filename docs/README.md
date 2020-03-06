# Documentation

The documentation is built with [R Markdown](https://rmarkdown.rstudio.com/) and hosted with [Github Pages](https://pages.github.com/).

R Markdown is an awesome tool that features:
- [knitr](https://yihui.org/knitr/): an **R** engine for embedding code chunks in Markdown files.
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

## Usage

```sh
# Generate book.pdf (via LaTeX)
make pdf

# Generate index.html
make html
```

## Directory Content

```
docs/
├── img/            # Image dir
├── include/        # TeX and HTML options
├── parts/          # Markdown content
├── _bookdown.yml   # bookdown options
├── _output.yml     # rmd output options
├── book.pdf        # PDF output
├── index.html      # HTML output
├── main.rmd        # main MD file
├── Makefile
└── README.md
```