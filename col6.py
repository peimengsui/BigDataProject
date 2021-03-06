from csv import reader 
import sys
from datetime import datetime
from pyspark import SparkContext

if __name__ == "__main__":
    sc = SparkContext()
    lines = sc.textFile(sys.argv[1], 1) 
    lines = lines.mapPartitions(lambda x: reader(x))
    header = lines.first()
    lines = lines.filter(lambda line: line != header)
    v6 = lines.map(lambda x: x[6])
    output6 = v6.map(lambda x : str(x)+" INT category VALID") 
    output6.saveAsTextFile("test6.out")