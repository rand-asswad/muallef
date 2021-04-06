# Makefile for Rmarkdown/bookdown

BOOK_SRC	:= main.rmd
SLIDES_SRC	:= presentation.md
OUTPUT_DIR	:= _out


all: pdf html reveal gitbook 
	@echo "rendering document html and pdf..."

pdf: ${BOOK_SRC}
	@echo "rendering pdf book..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::pdf_book', output_file='book.pdf')"
	@echo "done!"

html: ${BOOK_SRC}
	@echo "rendering html document..."
	[ -d ${OUTPUT_DIR} ] || mkdir ${OUTPUT_DIR}
	Rscript -e "bookdown::render_book('$<', 'bookdown::html_document2', output_file='${OUTPUT_DIR}/onepage.html')"
	@echo "done!"

gitbook: ${BOOK_SRC}
	@echo "rendering gitbook..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::gitbook')"
	@mv ${OUTPUT_DIR}/$(basename ${BOOK_SRC}).html ${OUTPUT_DIR}/index.html
	@echo "done!"

reveal: ${SLIDES_SRC}
	@echo "rendering revealjs presentation..."
	Rscript -e "rmarkdown::render('$<', 'revealjs::revealjs_presentation', output_dir='${OUTPUT_DIR}', output_file='presentation.html')"
	@mkdir -p ${OUTPUT_DIR}/img
	@cp img/logo_*.png ${OUTPUT_DIR}/img/
	@echo "done!"

clean:
	@-rm -rf ${OUTPUT_DIR} *_files *_cache
	@echo "cleaned book output."