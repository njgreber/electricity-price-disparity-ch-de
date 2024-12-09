# Build Docker image
build:
	docker-compose build

# Process data
process:
	docker-compose run app bash -c "jupyter nbconvert --to notebook --execute --inplace notebooks/1_process_data.ipynb"
	docker-compose run app bash -c "jupyter nbconvert --to notebook --execute --inplace notebooks/3_results.ipynb"
	docker-compose run app bash -c "jupyter nbconvert --to notebook --execute --inplace walkthrough.ipynb"

# Compile LaTeX files
compile:
	docker-compose run app bash -c "pdflatex -output-directory=report report/main.tex"
	docker-compose run app bash -c "pdflatex -output-directory=report report/beamer.tex"

# Full pipeline
run-all: build process compile
