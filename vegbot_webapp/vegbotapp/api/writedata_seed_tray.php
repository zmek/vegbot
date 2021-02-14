<?php
 echo "In file";

class seed_tray_data{
 public $link='';

 function __construct($temp, $status){
  $this->connect();
  $this->storeInDB($temp, $status);
 }

 function connect(){
  echo "Connecting to DB" . PHP_EOL;
  $this->link = mysqli_connect('31.170.123.74','vegbotsql_user1','PhAsL@B7vAx2qAw','vegbotsql') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'vegbotsql') or die('Cannot select the DB');
//  $this->link = mysqli_connect('localhost','arduino','XklBv4vu2mGe5xxG','') or die('Cannot connect to the DB');
//  mysqli_select_db($this->link,'garden_bot') or die('Cannot select the DB');
 }

 function storeInDB($temp, $status){
  echo "Inserting". $temp."and".$status. PHP_EOL;
  $query = "insert into seed_tray_temp set
  temp='".$temp."',
  status = '".$status."'
  ";
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }
}

# check whether temp has been sent
if($_GET['temp'] != ''){
  $link = mysqli_connect('31.170.123.74', 'vegbotsql_user1','PhAsL@B7vAx2qAw','vegbotsql');
//  $link = mysqli_connect('localhost', 'arduino','XklBv4vu2mGe5xxG','garden_bot');

  if (!$link) {
      echo "Error: Unable to connect to MySQL." . PHP_EOL;
      echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
      echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
      exit;
  }
 $seed_tray_data=new seed_tray_data(
   $_GET['temp'],
   $_GET['status'],
  );
}


?>
