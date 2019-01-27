
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<title>grade-notifier</title>
</head>
<body>
	<img width=200 src="http://www.ogeecheeriverkeeper.org/wp-content/uploads/2016/03/report-card-worry1-820x687.gif">
		<h1>CUNY Grade Notifier</h1>
		<form action=<?php echo $_SERVER['PHP_SELF']; ?> method="POST">
		Username: <input type="text" name="username">@login.cuny.edu<br>
		Password:&nbsp;<input type="password" name="password"><br>
		School:
		<select name="school">
			<option value="BAR01">Baruch College</option>
			<option value="BMC01">Borough of Manhattan CC</option>
			<option value="BCC01">Bronx CC</option>
			<option value="BKL01">Brooklyn College</option>
			<option value="CTY01">City College</option>
			<option value="CSI01">College of Staten Island</option>
			<option value="GRD01">Graduate Center</option>
			<option value="NCC01">Guttman CC</option>
			<option value="HOS01">Hostos CC</option>
			<option value="HTR01">Hunter College</option>
			<option value="JJC01">John Jay College</option>
			<option value="KCC01">Kingsborough CC</option>
			<option value="LAG01">LaGuardia CC</option>
			<option value="LEH01">Lehman College</option>
			<option value="MHC01">Macaulay Honors College</option>
			<option value="MEC01">Medgar Evers College</option>
			<option value="NYT01">NYC College of Technology</option>
			<option value="QNS01" selected>Queens College</option>
			<option value="QCC01">Queensborough CC</option>
			<option value="SOJ01">School of Journalism</option>
			<option value="SLU01">School of Labor&Urban Studies</option>
			<option value="LAW01">School of Law</option>
			<option value="MED01">School of Medicine</option>
			<option value="SPS01">School of Professional Studies</option>
			<option value="SPH01">School of Public Health</option>
			<option value="UAPC1">University Processing Center</option>
			<option value="YRK01">York College</option>
		</select><br>
	 	Phone Number: <input type="text" name="phone"><br>
		<input type="submit" name="submit">
	</form>
 <h3>Made with ❤️  by Ehud Adler</h3>
 <h4>Big thanks to @ericshermancs</h4>
</body>
<?php
	function display(){
     $arr = array();
     $cmd = '';
     if (gethostname() == "venus" || gethostname() == "mars") {
         require_once 'vendor/autoload.php';
         $dotenv = Dotenv\Dotenv::create(__DIR__);
         $dotenv->load();
         $account_pass = getenv('ACCOUNT_PASSWORD');
         $mars_user = getenv('MARS_USERNAME');
         $cmd = 'echo "'.$account_pass.'" | su -c "python3 /home/fa18/313/'.$mars_user.'/public_html/grade-notifier/Grade-Notifier/src/core/initializegn.py --username='.$_POST["username"].' --password='.$_POST["password"].' --school='.$_POST["school"].' --phone='.$_POST["phone"].' --prod=true" - '.$mars_user;

     } else {
         echo nl2br("********************\r\nRunning Local....\r\n********************\r\n");
         $cmd = 'python3 src/core/initializegn.py --username='.$_POST["username"].' --password='.$_POST["password"].' --school='.$_POST["school"].' --phone='.$_POST["phone"];
     }
     $message = exec($cmd, $arr);
     for($x = 0; $x < count($arr); $x++) {
         if (strpos($arr[$x], 'RENDER::') !== false) {
             echo htmlspecialchars(str_replace("RENDER::", "", $arr[$x]));
             echo "<br>";
         }
     }
		?>
		<?php
	}
	if(isset($_POST["submit"])){
		display();
	}
	?>
</body>
</html>
