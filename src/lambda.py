import firefly

from cortex.tcategorizer.predict import Classifier

imodel_dir = 'cortex/tcategorizer/trained_results_1502219150/'
imodel_seq = 70

iclf = Classifier(imodel_dir, seq_len = imodel_seq)

def predict_interest(payload):
	result = {}
	for s in payload:
		result[s] = iclf.predict(s)
	return result

def predict_sentiment(payload):
	result = {}
	for s in payload:
		result[s] = sclf.predict(s)
	return result