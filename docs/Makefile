doc: pdf html
	@echo "rendering document html and pdf..."

pdf: main.rmd
	@echo "rendering pdf book..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::pdf_book', output_file='report.pdf')"
	[ -f _book/report.pdf ] && mv _book/report.pdf report.pdf && rm -rf _book
	@echo "done!"

html: main.rmd
	@echo "rendering html document..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::html_document2')"
	@echo "done!"

gitbook: main.rmd
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
