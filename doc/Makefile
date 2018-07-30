build: examples
	expand-macros.py README.md.t ../README.md

.PHONY: examples
examples:
	cd examples; for file in *.py; do python3 $${file}; done
	cd examples; for dir in _*; do (cd $$dir && latexmk -c); done
