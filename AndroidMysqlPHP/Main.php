<?php
require "conn.php";
 $stmt = $conn->prepare("SELECT id,name,home_page,type FROM records;");
 if(mysqli_connect_errno())
 	die('Unable to connect to database '.mysqli_connect_error());

 //executing the query 
 $stmt->execute();
 
 //binding results to the query 
 $stmt->bind_result($id, $name, $home_page, $type);
 
 $products = array(); 
 
 //traversing through all the result 
 while($stmt->fetch()){
 $temp = array();
 $temp['id'] = $id; 
 $temp['name'] = $name; 
 $temp['home_page'] = $home_page; 
 $temp['type'] = $type; 
 array_push($products, $temp);
 }
 
 //displaying the result in json format 
 echo json_encode($products);
?>