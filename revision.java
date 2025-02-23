import java.util.LinkedHashMap;
import java.util.Map;
import java.util.TreeMap;

class Difffunction{
    /**
     * this function to practice map collection
     */
    void mapRevison(){
        Map<Integer,Integer> map=new TreeMap<>();
        map.put(1, 1);
        Map<Integer,Integer> newmap= new LinkedHashMap<>(0);
        newmap.putIfAbsent(2, 3);
        map.putAll(newmap);
        int valueof1= map.get(1);
        int valueofunknown= map.getOrDefault(4, 0);
        System.out.println(" get_function "+valueof1+"   getOrDefault_function "+valueofunknown);

        System.out.println("containsKey of 1 "+map.containsKey(2));
        System.out.println("containsValue  3"+map.containsValue(3));
        map.replace(1, 1, 4);
        map.remove(2);
        newmap.clear();

        //access for map keys only
        for(Integer num: map.keySet()){
            System.out.print(num);
        }
        System.out.println();
        //access for map values only
        for(Integer num: map.values()){
            System.out.print(num);
        }
        System.out.println();
        //access whole set
        for(Map.Entry<Integer,Integer> entry: map.entrySet()){
            System.out.print("entryset-"+entry+" key-"+entry.getKey()+" value"+entry.getValue());
        }
        System.out.println();
    }
}

public class revision {
    //map revision
    public static void main(String[] args) {
        Difffunction obj=new Difffunction();
        obj.mapRevison();
    }
}
