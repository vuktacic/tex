Repository Build Guidance for Agents
===================================

Purpose
-------
This file contains repository-wide instructions for automated agents (or maintainers) on how to build LaTeX labs so that all generated files are placed into an output directory instead of littering lab folders.

Recommended command (run from a lab directory, e.g. chemistry12/lab3c):

- latexmk -pdf -outdir=output -silent -f main.tex

Alternate command (if your latexmk doesn't support -outdir):

- latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode -output-directory=output" -silent -f main.tex

Agent rules
-----------
- Agents building labs should always use -outdir=output (or the pdflatex alternative) so build artifacts (PDF, logs, aux files) are written to output/ inside the lab directory.
- Run builds from within the lab folder (e.g. chemistry12/lab3c) to keep relative asset paths intact.
- Do not commit generated files produced by the build.

Why
---
- Centralises build artifacts per lab in a predictable place (output/), keeps source directories clean, and makes it trivial to find the produced PDF and logs.
