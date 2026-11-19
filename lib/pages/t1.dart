import 'package:flutter/material.dart';
import 'package:hotal/pages/home.dart';
class t1 extends StatelessWidget{
  const t1 ({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue,
        title: Text(
          'TABLE NO. 1',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      drawer: Drawer(
      child:ListView(
        children: [
          const DrawerHeader(
          decoration: BoxDecoration(
            color: Colors.blue,
             ), 
            child:Text(
              'ITEMS',
              style: TextStyle(
                color: Colors.white,
                
              ),
            ),
         
          ),
          ListTile(
            leading: const Icon(Icons.home),
            title:const Text('HOME'),
            onTap: (){
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context)=>const Homepage()),
              );
            },
          ),
        ],
      ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.blue,
        onTap: (index){
        if(index==0){
          Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(builder:(context)=>const Homepage()),
            (route)=>false,
          );
        }
        },
        items: const[
          BottomNavigationBarItem(
            icon:Icon(Icons.home),
            label:"HOME", 
            ),
            BottomNavigationBarItem(
              
              icon:Icon(Icons.table_restaurant),
              label: "TABLE", 
              ),
            BottomNavigationBarItem(
              
              icon:Icon(Icons.person),
              label: "Profile", 
              ),

        ],
        ),
    );
  }
}