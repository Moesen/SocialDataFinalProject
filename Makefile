lint:
	flake8 .

format:
	black .
	isort .

preprocess_data:
	python src/data_preproccess/join_energy_data.py --output_path data/preproccesed --input_path data/raw
	python src/data_preproccess/join_socio_data.py --output_path data/preproccesed --input_path data/raw 
	python src/data_preproccess/inter_extra_split_preprocess.py --output_path data/preproccesed --input_path data/raw --processed_path data/processed --x_extrap 5 --df_name ac_energy
	python src/data_preproccess/inter_extra_split_preprocess.py --output_path data/preproccesed --input_path data/raw --processed_path data/processed --x_extrap 5 --df_name pcc_energy
	python src/data_preproccess/inter_extra_split_preprocess.py --output_path data/preproccesed --input_path data/raw --processed_path data/processed --x_extrap 5 --df_name socio