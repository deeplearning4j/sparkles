#from naive import py2javaRDD, java2pyRDD
from fast_impl import java2pyRDD
from pydatavec.java_classes import SparkConf, SparkContext
from pydatavec.java_classes import ArrayList
import pyspark
import time
import numpy as np
import jumpy as jp



py_sc = pyspark.SparkContext(master='local[*]', appName='test')

config = SparkConf()
config.setAppName("test")
config.setMaster("local[*]")
java_sc = SparkContext(config)

data = ArrayList()
start = time.time()
for _ in range(10000):
    arr = jp.zeros((20, 10)).array
    data.add(arr)
end = time.time()
data_creation_time = end - start

print('Data creation: ' + str(data_creation_time))
start = time.time()
java_rdd = java_sc.parallelize(data)
end = time.time()
parallelize_time = end - start
print('java_sc.parallelize(data): ' + str(parallelize_time))

start = time.time()
py_rdd = java2pyRDD(java_rdd, py_sc)
end = time.time()
conversion_time = end - start
print('java2pyRDD(java_rdd, py_sc): ' + str(conversion_time))

data2 = py_rdd.collect()
assert len(data2) == data.size()
assert np.sum(data2) == 0.
