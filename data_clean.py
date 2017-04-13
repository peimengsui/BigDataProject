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
	f1 = lines.filter(lambda x : int(x[1][-4:])>=1900  if len(x[1])!=0 else True if len(x[1])==0 else False)
	f2 = f1.filter(lambda x : int(x[3][-4:])<2020 if len(x[3])!=0 else True if len(x[3])==0 else False)
	f3 = f2.filter(lambda x: (datetime.strptime(x[3], '%m/%d/%Y')-datetime.strptime(x[1], '%m/%d/%Y')).total_seconds()>=0 if len(x[3])!=0 and len(x[1])!=0 else True if len(x[1])==0 or len(x[3])==0 else False)
	f4 = f3.filter(lambda x: (datetime.strptime(x[5], '%m/%d/%Y')-datetime.strptime(x[1], '%m/%d/%Y')).total_seconds()>=0 if len(x[1])!=0 else True if len(x[1])==0 else False)

	#m1 = f4.map(lambda x: x if x[2]!= "24:00:00" and x[4]!="24:00:00" else x[0:2]+["00:00:00"]+x[3:] if x[4]!="24:00:00" else x[0:4]+["00:00:00"]+x[5:] if x[2]!="24:00:00" else x[0:2]+["00:00:00"]+x[3:4]+["00:00:00"]+x[5:])
	#f5 = m1.filter(lambda x: (datetime.strptime(x[3]+" "+x[4], '%m/%d/%Y %H:%M:%S')-datetime.strptime(x[1]+" "+x[2], '%m/%d/%Y %H:%M:%S')).total_seconds()>=0 if len(x[1])!=0 and len(x[3])!=0 else True if len(x[1])==0 or len(x[3])==0 else False)
	m1 = f4.map(lambda x: x[0:7]+["OTHER STATE LAWS"]+x[8:] if x[6]=='364' else x)
	m2 = m1.map(lambda x: x[0:7]+["KIDNAPPING"]+x[8:] if x[6]=='124' else x)
	m3 = m2.map(lambda x: x[0:7]+["CHILD ABANDONMENT"]+x[8:] if x[6]=='120' else x)
	m4 = m3.map(lambda x: x[0:7]+["NYS LAWS-UNCLASSIFIED VIOLATION"]+x[8:] if x[6]=='677' else x)
	m5 = m4.map(lambda x: x[0:7]+["ENDAN WELFARE INCOMP"]+x[8:] if x[6]=='345' else x)
	m6 = m5.map(lambda x: x[0:7]+["OTHER OFFENSES RELATED TO THEF"]+x[8:] if x[6]=='343' else x)
	ff1 = m6.filter(lambda x:x[2]!= "24:00:00")
	ff2 = ff1.filter(lambda x:x[4]!= "24:00:00")
	ff2.saveAsTextFile("cleaned_data.out")