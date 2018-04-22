<!DOCTYPE html>

<html>
<?php
$page = $_SERVER['PHP_SELF'];
$sec = "";
?>
<head>
<meta http-equiv="refresh" content=<?php echo $sec;?> URL=<?php echo $page;?>>
<style>

<!--
Imports Google fonts API for styling web-page.
--> 

	@import url('https://fonts.googleapis.com/css?family=Cuprum');
        body
        {
            font-family: arial,verdana,sans-serif,Georgia, "Times New Roman", Times, serif;
            
            text-align:center;
            background:#D8D8D8;
        }
        h1
        {
			font-size: 3em;
			color: #6A0888;
			font-family: 'Cuprum';
            text-shadow: 5px 5px 5px #aaaaaa;
        }
</style>
</head>
<body>
<img src='securitypic2.png' align="center" height="70%" width="50%">
<h1><b>Intruder Detection System</b></h1>



<?php
$username = "root";
$password = "";
$database = 'intrudersdatabase';

//Creates a connection to database with above credentials
$con=mysqli_connect("localhost",$username,$password) or die ("Unable to connect");
mysqli_select_db($con,$database) or die ("Could not select database");
$query = "SELECT * FROM detectionlogs";
$result=mysqli_query($con,$query);
$num=mysqli_num_rows($result);
mysqli_close($con);?>

<!-- Creates a table here where all data will be displayed
-->
<table  cellspacing="0" border=6 align=center width="65%" style ="background-color: #A9BCF5" >
<tr style= "background-color:#A4A4A4"> <th><font  size="5" div style="color:#0431B4" face="Arial, Helvetica, sans-serif">Date</font></th>
<th><font size="5" div style="color: #0431B4" face="Lato">Day</font></th>
<th><font size="5" div style="color:#0431B4" face="Lato">Time</font></th>
<th><font size="5" div style="color:#0431B4" face="Lato>Image</font></th>
</tr>



<?php
$i=0;
function mysqli_result($result, $row, $field=0) { 
    $result->data_seek($row); 
    $datarow = $result->fetch_array(); 
    return $datarow[$field]; 
}
while ($i < $num)
{
$datetime=mysqli_result($result,$i,"DateTime");
$date = date('jS F Y', strtotime($datetime));
$day = date('l', strtotime($datetime));
$time = date('H:i:s A', strtotime($datetime));
$image=mysqli_result($result,$i,"Image");?>
<tr>
<td><font size="4" face="Lato"><?php echo $date; ?></font></td>
<td><font size="4" face="Lato"><?php echo $day; ?></font></td>
<td><font size="4" face="Lato"><?php echo $time; ?></font></td>
<td width="20%"><?php echo '<a href="'.$image.'" target="_blank"><img src="'.$image.'" align=center height="20%" width=100%" style="display: block"></a>';?></td></tr>
<?php $i++;
}?>
</table>
</body>
</html>

 
