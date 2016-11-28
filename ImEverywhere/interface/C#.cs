using System;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

//How to execute Python modules in C#
//using System;
//using IronPython.Hosting;

//public class CallingPython
//{
//    public static void Main(string[] args)
//    {
//        var engine = Python.CreateEngine();
//        var scope = engine.CreateScope();
//        var source = engine.CreateScriptSourceFromString(
//            "def adder(arg1, arg2):\n" +
//            "   return arg1 + arg2\n" +
//            "\n" +
//            "class MyClass(object):\n" +
//            "   def __init__(self, value):\n" +
//            "       self.value = value\n");
//        source.Execute(scope);

//        var adder = scope.GetVariable<Func<object, object, object>>("adder");
//        Console.WriteLine(adder(2, 2));
//        Console.WriteLine(adder(2.0, 2.5));

//        var myClass = scope.GetVariable<Func<object, object>>("MyClass");
//        var myInstance = myClass("hello");

//        Console.WriteLine(engine.Operations.GetMember(myInstance, "value"));
//    }
//}

namespace QA
{
    class Program
    {
        static void Main(string[] args)
        {
            ScriptEngine pyEngine = Python.CreateEngine();
            var paths = pyEngine.GetSearchPaths();
            paths.Add(@"C:\Program Files (x86)\IronPython 2.7\Lib");
            paths.Add(@"C:\Program Files (x86)\IronPython 2.7\Lib\site-packages");
            pyEngine.SetSearchPaths(paths);
            var scope = pyEngine.CreateScope();
            var source = pyEngine.CreateScriptSourceFromFile("client.py");
            source.Execute(scope);

            var match = scope.GetVariable<Func<object, object, object>>("match");
            Console.WriteLine(match("什么是云账户", "Human"));
            Console.WriteLine(match("民生银行银联卡有效期是多久", "Human"));
            //var myClass = scope.GetVariable<Func<object, object>>("MyClass");
            //var myInstance = myClass("hello");
            //Console.WriteLine(engine.Operations.GetMember(myInstance, "value"));
            Console.ReadKey();
        }
    }
}
