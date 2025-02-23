//write program
class helloWorld{
    int data=1;
    public void show(){
        System.out.println("hello world - "+data);
    }
    public void addNew(int data){
        data= data + 100;
    }
    public static void main(String[] args){
        helloWorld obj=new helloWorld();
        
        //System.out.println("before change- "obj.data);
        obj.addNew(100);
        //System.out.println("after change- "obj.data);
        obj.show();
    }
    
}
