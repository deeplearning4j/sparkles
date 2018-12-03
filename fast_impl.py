import jnius_config
import os

sparkles_jar = 'java/sparkles/target/sparkles.jar'
sparkles_jar = os.path.abspath(sparkles_jar)

jnius_config.add_classpath(sparkles_jar)

import jumpy as jp
import numpy as np
import jnius
from pydatavec.java_classes import ArrayList

sparkles = jnius.autoclass('Utils')
ArrayDescriptor = jnius.autoclass('ArrayDescriptor')
DataType = jnius.autoclass('org.nd4j.linalg.api.buffer.DataBuffer$Type')

jp.disable_gc()


def java2pyRDD(java_rdd, py_sc):
    '''
    Arguments

    `java_rdd`: JavaRDD<INDArray> instance
    `py_sc`: Pyspark context instance

    Returns

    pyspark.RDD instance
    '''
    desc_rdd = sparkles.getArrayDescriptorRDD(java_rdd)
    descriptors = desc_rdd.collect()
    num_descriptors = descriptors.size()
    nparrays = []
    for i in range(num_descriptors):
        desc = descriptors.get(i)
        indarray = desc.getArray()
        jparray = jp.array(indarray)
        nparray = jparray.numpy()
        nparrays.append(nparray)
    return py_sc.parallelize(nparrays)


def py2javaRDD(py_rdd, java_sc):
    '''
    Arguments

    `py_rdd`: pyspark.RDD instance
    `java_sc`: JavaSparkContext instance

    Returns

    JavaRDD<INDArray> instance
    '''
    def np2desc(nparray):
        address = nparray.__array_interface__['data'][0]
        shape = nparray.shape
        stride = nparray.strides
        nptype = nparray.dtype
        if nptype == np.float32:
            dtype = "float"
        elif nptype == np.float64:
            dtype = "double"
        else:
            raise Exception("Unsupported data type: " + str(nptype))
        return (address, shape, stride, dtype)
    
    dtype_map = {
        "float": DataType.FLOAT,
        "double": DataType.DOUBLE
    }
    desc_rdd = py_rdd.map(np2desc)
    descriptors = desc_rdd.collect()
    arrlist = ArrayList()
    for d in descriptors:
        arrlist.add(ArrayDescriptor(d[0], d[1], d[2], dtype_map[d[3]]))
    java_rdd = java_sc.parallelize(arrlist)
    java_rdd = sparkles.getArrayRDD(java_rdd)
    return java_rdd
