import 'package:flutter/material.dart';
import 'package:hotal/pages/home.dart';
class t5 extends StatelessWidget{
  const t5 ({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue,
        title: Text(
          'TABLE NO. 5',
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
        ],
      ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.blue,
        
        unselectedItemColor: Colors.grey,
        currentIndex: 1,
        onTap: (index){
          if(index==0){
          Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(builder: (context)=>const Homepage()),
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
              icon: Icon(Icons.table_restaurant),
              label: 'TABLE',
            ),
            BottomNavigationBarItem(
            icon:Icon(Icons.person),
            label:"PROFILE", 
            ),
        ],
        ),
    );
  }
}