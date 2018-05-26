
all: index.rmd
	@echo "rendering..."
	Rscript -e "rmarkdown::render('$<', c('pdf_document', 'html_document'))"
	@echo "done!"

pdf: index.rmd
	@echo "rendering pdf..."
	Rscript -e "rmarkdown::render('$<', 'pdf_document')"
	@echo "done!"

html: index.rmd
	@echo "rendering html..."
	Rscript -e "rmarkdown::render('$<', 'html_document')"
	@echo "done!"

clean:
	@echo "cleaning..."
	rm *.pdf *.html
	@echo "done!"

