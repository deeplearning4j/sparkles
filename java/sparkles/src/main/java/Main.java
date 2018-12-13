import jdk.nashorn.internal.objects.annotations.Function;
import org.apache.commons.lang.ArrayUtils;
import org.apache.spark.SparkConf;
import org.apache.spark.SparkContext;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.util.ArrayUtil;

import java.util.ArrayList;
import java.util.List;

public class Main {


    public static void main(String[] args) {

        INDArray x = Nd4j.zeros(32, 10);
        INDArray y = Nd4j.zeros(32, 10);
        ArrayList data = new ArrayList();

        data.add(x);
        data.add(y);

        SparkConf conf = new SparkConf();
        conf.setMaster("local[*]");
        conf.setAppName("Test");
        JavaSparkContext jsc = new JavaSparkContext(conf);

        JavaRDD<INDArray> rdd = jsc.parallelize(data);
        List<INDArray> z = rdd.collect();
    }
}
