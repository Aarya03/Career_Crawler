<?php
require "conn.php";
$id=$_POST['id'];
$mysql_qry = "SELECT link FROM sites WHERE id = '$id'";
$result = mysqli_query($conn, $mysql_qry);
while ($row = mysqli_fetch_array($result)) {
    printf($row["link"].'#');
}
?>