//write program
class helloWorld{
    int time;
    public void show(){
        System.out.println("hello world - "+time);
    }
    public void addNew(){
        time=1;
    }
    public static void main(String[] args){
        helloWorld obj=new helloWorld();
        obj.addNew();
        obj.show();
    }
    
}
