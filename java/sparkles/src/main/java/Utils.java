import org.apache.spark.api.java.JavaRDD;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.cpu.nativecpu.NDArray;

public class Utils {

    public static JavaRDD<ArrayDescriptor> getArrayDescriptorRDD(JavaRDD<INDArray> indarrayRDD){
        return indarrayRDD.map(arr -> new ArrayDescriptor(arr));
    }

    public static  JavaRDD<INDArray> getArrayRDD(JavaRDD<ArrayDescriptor> arrayDescriptorRDD){
        return arrayDescriptorRDD.map(ad -> ad.getArray());
    }
}
