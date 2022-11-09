.PHONY: clean

conference_101719.pdf: *.tex bib.bib
	xelatex conference_101719 && \
	bibtex conference_101719 && \
	xelatex conference_101719 && \
	xelatex conference_101719
clean:
	rm *.aux *.log *.bbl *.blg *.lof *.lot *.out *.toc *.ilg *.nlo *.nls conference_101719.pdf -f
