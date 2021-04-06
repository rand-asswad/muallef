book: pdf gitbook
	@echo "rendering document html and pdf..."

pdf: main.rmd
	@echo "rendering pdf book..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::pdf_book', output_file='book.pdf')"
	[ -f book.pdf ] || ln -s out/book.pdf book.pdf
	@echo "done!"

html: main.rmd
	@echo "rendering html document..."
	[ -d out ] || mkdir out
	Rscript -e "bookdown::render_book('$<', 'bookdown::html_document2', output_file='out/onepage.html')"
	@echo "done!"

gitbook: main.rmd
	@echo "rendering gitbook..."
	Rscript -e "bookdown::render_book('$<', 'bookdown::gitbook')"
	mv out/main.html out/index.html
	@echo "done!"

reveal: presentation.md
	@echo "rendering revealjs presentation..."
	Rscript -e "rmarkdown::render('$<', 'revealjs::revealjs_presentation', output_dir='out', output_file='presentation.html')"
	@mkdir -p out/img
	@cp img/logo_*.png out/img/
	@echo "done!"

clean:
	@-rm -rf out _book *_files *_cache book.pdf
	@echo "cleaned book output."