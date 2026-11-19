import 'package:flutter/material.dart';
import 'package:hotal/pages/home.dart';
class t4 extends StatelessWidget{
  const t4 ({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue,
        title: Text(
          'TABLE NO. 4',
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
            leading: Icon(Icons.home),
            title: const Text('HOME'),
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
    );
  }
}