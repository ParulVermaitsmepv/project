import 'package:flutter/material.dart';
import 'package:hotal/pages/t1.dart';
import 'package:hotal/pages/t2.dart';
import 'package:hotal/pages/t3.dart';
import 'package:hotal/pages/t4.dart';
import 'package:hotal/pages/t5.dart';

class Homepage extends StatelessWidget{
  const Homepage({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 102, 169, 224),
      title: Text(
        'SPICY MIST',
        style: TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
          fontSize: 30,
        ),
      ),
      centerTitle: true,
      ),
      drawer: Drawer(
        child: ListView(
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color:Colors.blue,
                ),
                child:Text(
                  'SPICY MIST',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                
                
            ),
          ],
        ),
      ),
      body:  Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(height :10),
            ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.blue,
    foregroundColor: Colors.white,
    padding: const EdgeInsets.all(20),
    elevation: 8,
    shadowColor: Colors.black,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10),
    ),
  ),
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const t1()),
    );
  },
  child: const Text('TABLE NO 1'),
),

const SizedBox(height: 10),
ElevatedButton(
  style:ElevatedButton.styleFrom(
    backgroundColor: Colors.blue,
    foregroundColor: Colors.white,
    padding: EdgeInsets.all(20),
    shadowColor: Colors.black,
    elevation: 8,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10),
    ),
      ),
  onPressed: (){
    Navigator.push(
      context,
      MaterialPageRoute(builder:(context) => const t2 ()),
    );
  },
   child:const Text('TABLE NO. 2'), 
   ),
   const SizedBox(height :10),
            ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.blue,
    foregroundColor: Colors.white,
    padding: const EdgeInsets.all(20),
    elevation: 8,
    shadowColor: Colors.black,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10),
    ),
  ),
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const t3()),
    );
  },
  child: const Text('TABLE NO 3'),
),
const SizedBox(height :10),
            ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.blue,
    foregroundColor: Colors.white,
    padding: const EdgeInsets.all(20),
    elevation: 8,
    shadowColor: Colors.black,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10),
    ),
  ),
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const t4()),
    );
  },
  child: const Text('TABLE NO 4'),
),
const SizedBox(height :10),
            ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.blue,
    foregroundColor: Colors.white,
    padding: const EdgeInsets.all(20),
    elevation: 8,
    shadowColor: Colors.black,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10),
    ),
  ),
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const t5()),
    );
  },
  child: const Text('TABLE NO 5'),
),
          ],
        ),
        
      ),
      backgroundColor: const Color.fromARGB(255, 207, 227, 243),
    );
  }
}