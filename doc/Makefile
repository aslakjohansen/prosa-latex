TARGETS = \
	introduction_presentation.pdf \


all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch dummy~ d.aux d.log d.nav d.out d.snm d.toc d.vrb
	rm        *~ *.aux *.log *.nav *.out *.snm *.toc *.vrb


introduction_presentation.pdf: introduction_presentation.tex introduction_contents.tex introduction_shared.tex shared.tex
	lualatex  -shell-escape introduction_presentation.tex

