import xgboost as xgb
import numpy as np

dtest = xgb.DMatrix('data.svm.test')

bst = xgb.Booster()

bst.load_model('bst.model')
preds = bst.predict(dtest)

labels = dtest.get_label()

errors = []
for p,l in zip(preds,labels):
	errors.append( round(p)-l > 0 )

print "Accuracy: " + str(1 - np.sum(errors)/float(len(preds)))
