import xgboost as xgb
import numpy as np

import xgboost as xgb

# load date
dtrain = xgb.DMatrix('data.svm.train')
dtest = xgb.DMatrix('data.svm.test')

def evalerror(preds, dtrain):
	labels = dtrain.get_label()
	errors = []
	for p,l in zip(preds,labels):
		errors.append( round(p)-l > 0 )
	return 'error', float(np.sum(errors)) / len(preds)
	# return 'error', float(sum(labels != (preds > 0.0))) / len(labels)

# set param
params = {'max_depth': 10, 'eta': 0.3, 'objective': 'reg:linear'}
evallist = [(dtest, 'eval'), (dtrain, 'train')]
num_round = 100;
bst = xgb.train(params, dtrain, num_round, evallist, None, evalerror)
bst.save_model('bst.model')
bst.dump_model('bst.dump.txt')
