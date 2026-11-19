import 'package:flutter/material.dart';
import 'package:hotal/pages/home.dart';
import 'package:hotal/pages/t1.dart';
import 'package:hotal/pages/t2.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return MaterialApp(

      debugShowCheckedModeBanner: false,
      home:Homepage(),
    );
  }
  }

