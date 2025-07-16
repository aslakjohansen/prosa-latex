TARGETS = \
	introduction_presentation.pdf \
	intermediate_presentation.pdf \


all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch dummy~ d.aux d.log d.nav d.out d.snm d.toc d.vrb d.minted
	rm        *~ *.aux *.log *.nav *.out *.snm *.toc *.vrb *.minted


introduction_presentation.pdf: introduction_presentation.tex introduction_contents.tex introduction_shared.tex shared.tex Makefile
	lualatex  -shell-escape introduction_presentation.tex
	lualatex  -shell-escape introduction_presentation.tex

intermediate_presentation.pdf: intermediate_presentation.tex intermediate_contents.tex intermediate_shared.tex shared.tex Makefile
	lualatex  -shell-escape intermediate_presentation.tex
	lualatex  -shell-escape intermediate_presentation.tex

