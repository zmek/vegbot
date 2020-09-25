<?php

class mkr1010{
 public $link='';

 function __construct($loc, $temp, $temp_dht22, $humidity, $humidity_dht22, $pressure, $illuminance, $uva, $uvb, $uvindex, $rssi, $millis, $filename){
  $this->connect();
  $this->storeInDB($loc, $temp, $temp_dht22, $humidity, $humidity_dht22, $pressure, $illuminance, $uva, $uvb, $uvindex, $rssi, $millis, $filename);
 }

 function connect(){
  echo "Connecting to DB" . PHP_EOL;
  $this->link = mysqli_connect('31.170.123.74','vegbotsql_user1','PhAsL@B7vAx2qAw','vegbotsql') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'vegbotsql') or die('Cannot select the DB');
//  $this->link = mysqli_connect('localhost','arduino','XklBv4vu2mGe5xxG','') or die('Cannot connect to the DB');
//  mysqli_select_db($this->link,'garden_bot') or die('Cannot select the DB');
 }

 function storeInDB($loc,$temp, $temp_dht22, $humidity, $humidity_dht22, $pressure, $illuminance, $uva, $uvb, $uvindex, $rssi, $millis, $filename){
  echo "Inserting". $temp."and".$humidity. PHP_EOL;
  $query = "insert into arduino_data set loc='".$loc."',
  humidity='".$humidity."',
  humidity_dht22='".$humidity_dht22."',
  temp='".$temp."',
  temp_dht22='".$temp_dht22."',
  pressure='".$pressure."',
  illuminance= '".$illuminance."',
  uva = '".$uva."',
  uvb = '".$uvb."',
  uvindex = '".$uvindex."',
  rssi = '".$rssi."',
  millis = '".$millis."',
  filename = '".$filename."'
  ";
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }
}
if($_GET['temp'] != '' and  $_GET['humidity'] != ''){
  $link = mysqli_connect('31.170.123.74', 'vegbotsql_user1','PhAsL@B7vAx2qAw','vegbotsql');
//  $link = mysqli_connect('localhost', 'arduino','XklBv4vu2mGe5xxG','');

  if (!$link) {
      echo "Error: Unable to connect to MySQL." . PHP_EOL;
      echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
      echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
      exit;
  }
 $mkr1010=new mkr1010(
   $_GET['loc'],
   $_GET['temp'],
   $_GET['temp_dht22'],
   $_GET['humidity'],
   $_GET['humidity_dht22'],
   $_GET['pressure'],
   $_GET['illuminance'],
   $_GET['uva'],
   $_GET['uvb'],
   $_GET['uvindex'],
   $_GET['rssi'],
   $_GET['millis'],
   $_GET['filename'],
  );
}


?>
