<?php 
$con = mysqli_connect("localhost","root","admin","hackathon");

if (mysqli_connect_errno())
  {
  echo "Failed to connect to Database: " . mysqli_connect_error();
  }
  
?>