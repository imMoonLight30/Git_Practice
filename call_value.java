public class call_value {
    int data=1;
    public void show(){
        System.out.println("hello world - "+data);
    }
    public void addNew(int data){
        data= data + 100;
    }
}

class Operation{  
 int data=50;  
  
 void change(int data){  
 data=data+100;//changes will be in the local variable only  
 System.out.print(data);
 }  
     
 public static void main(String args[]){  
   Operation op=new Operation();  
   call_value obj = new call_value();
   obj.show();
   obj.addNew(100);
   obj.show();

   
   System.out.println("before change "+op.data);  
   op.change(500);  
   System.out.println("after change "+op.data);  
  
 }  
} 
