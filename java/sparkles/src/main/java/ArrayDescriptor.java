import org.bytedeco.javacpp.DoublePointer;
import org.bytedeco.javacpp.FloatPointer;
import org.bytedeco.javacpp.Pointer;
import org.nd4j.linalg.api.buffer.DataBuffer;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.nativeblas.NativeOps;
import org.nd4j.nativeblas.NativeOpsHolder;

public class ArrayDescriptor {

    private long address;
    private long[] shape;
    private long[] stride;
    DataBuffer.Type type;
    private static NativeOps nativeOps = NativeOpsHolder.getInstance().getDeviceNativeOps();

    public ArrayDescriptor(INDArray array) throws Exception{
        this(array.data().address(), array.shape(), array.stride(), array.data().dataType());
    }

    public ArrayDescriptor(long address, long[] shape, long[] stride, DataBuffer.Type type) throws Exception{
        this.address = address;
        this.shape = shape;
        this.stride = stride;
        this.type = type;
        if (type != DataBuffer.Type.FLOAT && type != DataBuffer.Type.DOUBLE){
            throw new Exception("Unsupported type.");
        }
    }
    public long getAddress(){
        return address;
    }

    public long[] getShape(){
        return shape;
    }

    public long[] getStride(){
        return stride;
    }

    private long size(){
        long s = 1;
        for (long d: shape){
            s *= d;
        }
        return s;
    }

    public INDArray getArray(){
        Pointer ptr = nativeOps.pointerForAddress(address);
        DataBuffer buff;
        switch(type){
            case FLOAT:
                FloatPointer floatPtr = new FloatPointer(ptr);
                buff = Nd4j.createBuffer(floatPtr, size());
                break;
            default:
                DoublePointer doublePtr = new DoublePointer(ptr);
                buff = Nd4j.createBuffer(doublePtr, size());
                break;

        }
        return Nd4j.create(buff, shape, stride, 0);
    }

}
