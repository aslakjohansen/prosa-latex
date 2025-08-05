TARGETS = \
	introduction_presentation.pdf \
	intermediate_presentation.pdf \

INTERMEDIATE_DEPS = \
	../src/table_heatmap/code.txt \
	../src/table_heatmap/code.tex \
	figs/sdi.tex \


all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch dummy~ d.aux d.log d.nav d.out d.snm d.toc d.vrb d.minted
	rm        *~ *.aux *.log *.nav *.out *.snm *.toc *.vrb *.minted


../src/table_heatmap/code.txt: ../src/table_heatmap/code.py
	../src/table_heatmap/code.py > ../src/table_heatmap/code.txt

../src/table_heatmap/code.tex: ../src/table_heatmap/process.py ../src/table_heatmap/code.txt
	../src/table_heatmap/process.py ../src/table_heatmap/code.txt ../src/table_heatmap/code.tex

figs/sdi.tex: figs/sdi.graphml ../bin/generate-sdi-tikz-figure.py
	../bin/generate-sdi-tikz-figure.py figs/sdi.graphml figs/sdi.tex


introduction_presentation.pdf: introduction_presentation.tex introduction_contents.tex introduction_shared.tex shared.tex Makefile
	lualatex  -shell-escape introduction_presentation.tex
	lualatex  -shell-escape introduction_presentation.tex

intermediate_presentation.pdf: intermediate_presentation.tex intermediate_contents.tex intermediate_shared.tex shared.tex Makefile ${INTERMEDIATE_DEPS}
	lualatex  -shell-escape intermediate_presentation.tex
	lualatex  -shell-escape intermediate_presentation.tex

