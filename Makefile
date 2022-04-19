lint:
	flake8 .

format:
	black .
	isort .

preprocess_data:
	python src/data_preproccess/join_energy_data.py --output_path data/preproccesed --input_path data/raw
	python src/data_preproccess/join_socio_data.py --output_path data/preproccesed --input_path data/raw --x_extrap 5