book: pdf gitbook
	@echo "rendering document html and pdf..."

pdf: main.rmd
	@echo "rendering pdf book..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::pdf_book', output_file='book.pdf')"
	@echo "done!"

html: main.rmd
	@echo "rendering html document..."
	[ -d _out ] || mkdir _out
	Rscript -e "bookdown::render_book('$<', 'bookdown::html_document2', output_file='_out/onepage.html')"
	@echo "done!"

gitbook: main.rmd
	@echo "rendering gitbook..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::gitbook')"
	mv _out/main.html _out/index.html
	@echo "done!"

reveal: presentation.md
	@echo "rendering revealjs presentation..."
	Rscript -e "rmarkdown::render('$<', 'revealjs::revealjs_presentation', output_dir='_out', output_file='presentation.html')"
	@mkdir -p _out/img
	@cp img/logo_*.png _out/img/
	@echo "done!"

clean:
	@-rm -rf _out _book *_files *_cache
	@echo "cleaned book output."