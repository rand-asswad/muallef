doc: pdf html
	@echo "rendering document html and pdf..."

pdf: index.rmd
	@echo "rendering pdf book..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::pdf_book', output_file='book.pdf')"
	[ -f book/book.pdf ] && mv book/book.pdf report.pdf
	@echo "done!"

html: index.rmd
	@echo "rendering html document..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::html_document2', output_file='index.html')"
	@echo "done!"

gitbook: index.rmd
	@echo "rendering gitbook..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::gitbook')"
	@echo "done!"

beamer: presentation.md
	@echo "rendering beamer presentation..."
	Rscript -e "rmarkdown::render('$<', 'beamer_presentation')"
	@echo "done!"

reveal: presentation.md
	@echo "rendering revealjs presentation..."
	Rscript -e "rmarkdown::render('$<', 'revealjs::revealjs_presentation')"
	@echo "done!"
