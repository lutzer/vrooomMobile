#!/usr/bin/env python3

"""Convert ARFF feature vector file to SVM feature vector file.
@author Dat Hoang
@date March 2011"""

import sys
import csv
from optparse import OptionParser


ARFF_DELIMITER = ','
SVM_DELIMITER = ' '
SKIP_LINE_ELEMENTS = 3


def transform(arff_fp, svm_fp):
	"""Transform every training instance of ARFF file to SVM instances
	   and return all the field mappings collected."""
	reader = csv.reader(arff_fp, delimiter=ARFF_DELIMITER)
	category_table = {}
	counter = 0

	for line in reader:

		if not line or line[0][0]=='@':
			continue #ignore header lines

		*rest, category = line
		if category not in category_table:
			numeric_category = category_table[category] = counter = counter + 1
		else:
			numeric_category = category_table[category]

		# delete the first elements in line
		del rest[:SKIP_LINE_ELEMENTS]
		values = SVM_DELIMITER.join("%s:%s"%(i+1, s)
			for i, s in enumerate(rest, start=0) if float(s)!=0.0)
		svm_fp.write("%s %s\n" % (numeric_category, values))

		# values = list()
		# for i, s in enumerate(rest, start=2):
		# 	values.append(SVM_DELIMITER.join("%s:%s"%(i, s)))
		# 	# print(SVM_DELIMITER.join("%s:%s"%(i, s)))
		# svm_fp.write("%s %s\n" % (numeric_category, values))
		# # 	values.append(SVM_DELIMITER.join("%s:%s"%(i, s))

	return category_table

def main():
	parser = OptionParser(
		usage="""Usage: %prog <fields> <arff-file> <svm-file>
			<arff-file> := arff source file (- := /dev/stdin)
			<svm-file> := svm destination file (- := /dev/stdout)
			<fields> := field-mappings destination file (- := /dev/stderr)""")

	(_, args) = parser.parse_args()
	if len(args) != 2:
		parser.print_usage(file=sys.stderr)
		return 1

	arff_file = "/dev/stdin" if args[0]=='-' else args[0]
	svm_file = "/dev/stdout" if args[1]=='-' else args[1]

	with open(arff_file, 'r') as arff_fp, open(svm_file, 'w') as svm_fp:
		fields_table = transform(arff_fp, svm_fp)

	if len(args) > 2:
		fields_file = "/dev/stderr" if args[3]=='-' else args[3]
		with open(fields_file, 'w') as fields_fp:
			for k, v in fields_table.items():
				fields_fp.write("%s\t%s\n" % (v, k))

	return 0

if __name__=="__main__":
	sys.exit(main())
