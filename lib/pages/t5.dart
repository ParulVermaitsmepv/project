import 'package:flutter/material.dart';
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
    );
  }
}