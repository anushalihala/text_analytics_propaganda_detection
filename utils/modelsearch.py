def get_metrics(y, y_pred, metrics):
    results = {}
    for metric, metric_fn in metrics.items():
        results[metric] = metric_fn(y, y_pred)
    return results
	
def print_metrics(scores):
    for metric, score in scores.items():
        print(metric, "=", score)
		
def model_search(model_list, train, metrics, valid=None):
	models_dict = {}
	models_info = {}
	
	for name, desc, model in model_list:
		print("Fitting",name,"...")
		models_dict[name] = model.fit(train[0],train[1])
		models_info[name] = {}
		models_info[name]['description'] = desc
		
		train_scores = get_metrics(train[1], model.predict(train[0]), metrics)
		print('Training scores:')
		print_metrics(train_scores)
		for metric, score in train_scores.items():
			models_info[name]['train_'+metric] = score
		
		if valid is not None:
			valid_scores = get_metrics(valid[1], model.predict(valid[0]), metrics)
			print('Validation scores:')
			print_metrics(valid_scores)
			for metric, score in valid_scores.items():
				models_info[name]['valid_'+metric] = score
		print()
	return (models_dict, models_info)