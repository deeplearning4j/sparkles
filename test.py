from fast_impl import java2pyRDD as java2pyRDD2, py2javaRDD as py2javaRDD2
from naive_impl import java2pyRDD as java2pyRDD1, py2javaRDD as py2javaRDD1
from pydatavec.java_classes import SparkConf, SparkContext
from pydatavec.java_classes import ArrayList
import jumpy as jp
import numpy as np
import pyspark
import pytest


class TestConverters(object):
    
    @pytest.fixture(scope='module')
    def java_sc(self):
        config = SparkConf()
        config.setAppName("test")
        config.setMaster("local[*]")
        return SparkContext(config)

    @pytest.fixture(scope='module')
    def py_sc(self):
        return pyspark.SparkContext(master='local[*]', appName='test')

    def test_java2pyRDD1(self, java_sc, py_sc):
        data = ArrayList()

        for _ in range(100):
            arr = jp.zeros((20, 10)).array
            data.add(arr)

        java_rdd = java_sc.parallelize(data)
        py_rdd = java2pyRDD1(java_rdd, py_sc)

        data2 = py_rdd.collect()
        assert len(data2) == data.size()
        assert np.sum(data2) == 0.

    def test_java2pyRDD2(self, java_sc, py_sc):
        data = ArrayList()

        for _ in range(100):
            arr = jp.zeros((20, 10)).array
            data.add(arr)

        java_rdd = java_sc.parallelize(data)
        py_rdd = java2pyRDD2(java_rdd, py_sc)

        data2 = py_rdd.collect()
        assert len(data2) == data.size()
        assert np.sum(data2) == 0.

    def test_py2javaRDD1(self, java_sc, py_sc):
        data = [np.zeros((20, 10)) for _ in range(100)]

        py_rdd = py_sc.parallelize(data)
        java_rdd = py2javaRDD1(py_rdd, java_sc)

        data2 = java_rdd.collect()
        n = data2.size()
        assert n == len(data)
        s = 0.
        for i in range(n):
            s += float(jp.sum(data2.get(i)))
        assert s == 0.

    def test_py2javaRDD2(self, java_sc, py_sc):
        data = [np.zeros((20, 10)) for _ in range(100)]

        py_rdd = py_sc.parallelize(data)
        java_rdd = py2javaRDD2(py_rdd, java_sc)

        data2 = java_rdd.collect()
        n = data2.size()
        assert n == len(data)
        s = 0.
        for i in range(n):
            s += float(jp.sum(data2.get(i)))
        assert s == 0.

if __name__ == '__main__':
    pytest.main([__file__])
