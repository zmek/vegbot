<?php

class mkr1010{
 public $link='';

 function __construct($loc, $temp, $humidity, $pressure, $illuminance, $uva, $uvb, $uvindex, $rssi){
  $this->connect();
  $this->storeInDB($loc, $temp, $humidity, $pressure, $illuminance, $uva, $uvb, $uvindex, $rssi);
 }

 function connect(){
  echo "Connecting to DB" . PHP_EOL;
  $this->link = mysqli_connect('localhost','vegbotsql_user1','PhAsL@B7vAx2qAw','') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'arduino_data') or die('Cannot select the DB');
 }

 function storeInDB($loc, $temp, $humidity, $pressure, $illuminance, $uva, $uvb, $uvindex, $rssi){
  echo "Inserting". $temp."and".$humidity. PHP_EOL;
  $query = "insert into arduino_data set loc='".$loc."',
  humidity='".$humidity."',
  temp='".$temp."',
  pressure='".$pressure."',
  illuminance= '".$illuminance."',
  uva = '".$uva."',
  uvb = '".$uvb."',
  uvindex = '".$uvindex."',
  rssi = '".$rssi."'
  ";
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }

echo "In php file";

}
if($_GET['temperature'] != '' and  $_GET['humidity'] != ''){
  $link = mysqli_connect('localhost', 'vegbotsql_user1','PhAsL@B7vAx2qAw','');

  if (!$link) {
      echo "Error: Unable to connect to MySQL." . PHP_EOL;
      echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
      echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
      exit;
  }
 $mkr1010=new mkr1010(
   $_GET['loc'],
   $_GET['temp'],
   $_GET['humidity'],
   $_GET['pressure'],
   $_GET['illuminance'],
   $_GET['uva'],
   $_GET['uvb'],
   $_GET['uvindex'],
   $_GET['rssi']
  );
}


?>
