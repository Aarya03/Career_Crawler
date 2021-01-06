<?php
require "conn.php";
$name = $_POST["name"];
$surname = $_POST["surname"];
$age = $_POST["age"];
$username = $_POST["username"];
$password = $_POST["password"];
if(strlen($name)==0 || strlen($surname)==0 ||strlen($age)==0 ||strlen($username)==0 ||strlen($password)==0)
	die('Error1');
if(strlen($password)<8)
	die('Error2');
$password=md5($password);
$mysql_query = "INSERT INTO user_data(firstname,surname,location,username,password)
				VALUES('$name','$surname','$age','$username','$password')";
echo "\n";
if($conn->query($mysql_query)===TRUE)
	echo "Insert Successful";
else
	echo "Error: ".$mysql_query."<br>".$conn->error; 
$conn->close();
?>