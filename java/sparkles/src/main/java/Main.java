import jdk.nashorn.internal.objects.annotations.Function;
import org.apache.commons.lang.ArrayUtils;
import org.apache.spark.SparkConf;
import org.apache.spark.SparkContext;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.nd4j.linalg.api.buffer.DataType;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.util.ArrayUtil;

import java.util.ArrayList;
import java.util.List;

public class Main {


    public static void main(String[] args)throws Exception {

        INDArray x = Nd4j.zeros(DataType.DOUBLE,10, 10);
        ArrayDescriptor desc = new ArrayDescriptor(x);

        INDArray y = desc.getArray();

        System.out.println(y.shape());

        System.out.println(y.getDouble(0));

        /*
        INDArray y = Nd4j.zeros(32, 10);
        ArrayList data = new ArrayList();

        data.add(x);
        data.add(y);

        SparkConf conf = new SparkConf();
        conf.setMaster("local[*]");
        conf.setAppName("Test");
        JavaSparkContext jsc = new JavaSparkContext(conf);
        JavaRDD<INDArray> rdd = jsc.parallelize(data);
        JavaRDD<ArrayDescriptor> descRdd = Utils.getArrayDescriptorRDD(rdd);
        rdd = Utils.getArrayRDD(descRdd);
        List<INDArray> z = rdd.collect();
        jsc.stop();
        System.out.println(z.get(0));
        */
    }
}
