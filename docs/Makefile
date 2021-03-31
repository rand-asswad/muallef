book: pdf gitbook
	@echo "rendering document html and pdf..."

pdf: index.rmd
	@echo "rendering pdf book..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::pdf_book', output_file='book.pdf')"
	[ -f book.pdf ] || ln -s book/book.pdf book.pdf
	@echo "done!"

html: index.rmd
	@echo "rendering html document..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::html_document2', output_file='onepage.html')"
	[ -f index.html ] || ln -s .redirect index.html
	@echo "done!"

gitbook: index.rmd
	@echo "rendering gitbook..."
	[ ! -f index.html ] || rm index.html
	Rscript -e "bookdown::render_book('$<', 'bookdown::gitbook')"
	@ln -s .redirect index.html
	@echo "done!"

reveal: presentation.md
	@echo "rendering revealjs presentation..."
	Rscript -e "rmarkdown::render('$<', 'revealjs::revealjs_presentation')"
	@echo "done!"

clean:
	@-rm -rf book _bookdown_files index.html book.pdf
	@echo "cleaned book output."