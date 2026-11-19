import 'package:flutter/material.dart';
import 'package:hotal/pages/home.dart';

class t2 extends StatelessWidget{
  const t2 ({super.key});
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue,
        title: Text(
          'TABLE NO. 2',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
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