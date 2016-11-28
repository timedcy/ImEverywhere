import javax.script.*;  
  
import org.python.core.PyFunction;  
import org.python.core.PyInteger;  
import org.python.core.PyObject;  
import org.python.util.PythonInterpreter;  
  
import java.io.*;  
import static java.lang.System.*;  
public class FirstJavaScript  
{  
    public static void main(String args[])  
    {  
          
        PythonInterpreter interpreter = new PythonInterpreter();  
        interpreter.execfile("client.py");  
        PyFunction func = (PyFunction)interpreter.get("test",PyFunction.class);  
  
        String question = "什么是云账户"
        String username	= "Human"	
        PyObject pyobj = func.__call__(new PyInteger(question), new PyInteger(username));  
        System.out.println("anwser = " + pyobj.toString());  
  
  
    }//main  
}  
