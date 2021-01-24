<?php
require "conn.php";
$user_name = $_POST["user_name"];
$user_pass = $_POST["password"];
$user_pass=md5($user_pass);
$mysql_qry = "SELECT * FROM user_data WHERE username LIKE '$user_name' AND password LIKE '$user_pass'";
$result = mysqli_query($conn, $mysql_qry);
echo "\n";
if(mysqli_num_rows($result)>0)
	echo "Login Success";
else
	echo "Wrong Username or Password";
?>