TARGETS = \
	introduction_presentation.pdf \
	intermediate_presentation.pdf \

INTRODUCTION_DEPS = \
	./figs/vector.pdf \

INTERMEDIATE_DEPS = \
	../src/table_heatmap/code.txt \
	../src/table_heatmap/code.tex \
	figs/sdi.tex \
	.intermediate.timestamp \


all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch dummy~ d.aux d.log d.nav d.out d.snm d.toc d.vrb d.minted
	rm        *~ *.aux *.log *.nav *.out *.snm *.toc *.vrb *.minted


.intermediate.timestamp: ../bin/generate-tex-includes intermediate_*.tex ./figs/vector0.svg
	cd .. ; ./bin/generate-tex-includes PDF doc/intermediate_presentation.tex doc
	touch .intermediate.timestamp

./figs/vector.pdf: ./figs/vector.svg
	inkscape ./figs/vector.svg -z -D -o ./figs/vector.pdf

./figs/vector0.svg: ../bin/process-vector.py ./figs/vector.svg
	../bin/process-vector.py


../src/table_heatmap/code.txt: ../src/table_heatmap/code.py
	../src/table_heatmap/code.py > ../src/table_heatmap/code.txt

../src/table_heatmap/code.tex: ../src/table_heatmap/process.py ../src/table_heatmap/code.txt
	../src/table_heatmap/process.py ../src/table_heatmap/code.txt ../src/table_heatmap/code.tex

figs/sdi.tex: figs/sdi.graphml ../bin/generate-sdi-tikz-figure.py
	../bin/generate-sdi-tikz-figure.py figs/sdi.graphml figs/sdi.tex


introduction_presentation.pdf: introduction_presentation.tex introduction_contents.tex introduction_*.tex shared.tex Makefile ${INTRODUCTION_DEPS}
	lualatex  -shell-escape introduction_presentation.tex
	lualatex  -shell-escape introduction_presentation.tex

introduction_handouts.pdf: introduction_handouts.tex introduction_contents.tex introduction_*.tex shared.tex Makefile ${INTRODUCTION_DEPS}
	lualatex  -shell-escape introduction_handouts.tex
	lualatex  -shell-escape introduction_handouts.tex

intermediate_presentation.pdf: intermediate_presentation.tex intermediate_contents.tex intermediate_*.tex shared.tex Makefile ${INTERMEDIATE_DEPS}
	lualatex  -shell-escape intermediate_presentation.tex
	lualatex  -shell-escape intermediate_presentation.tex

