<?php
    $arr = array();
    $status = '';
    $title = '';
    $message = '';
    $landing = !isset($_POST["submit"]);

    function display(){
        global $arr, $status, $title, $message;
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

        for ($x = 0; $x < count($arr); $x++) {
            if (strpos($arr[$x], 'RENDER::') !== false) {

                    // Remove RENDER::
                $worend = str_replace("RENDER::", "", $arr[$x]);

                    // Parse the text to get the status and title
                    //
                    // Regex matches the following:
                    // --<key>="<value>" (Will match)
                    // --<key>=<value> (Will not match)
                    //
                    // Contain a single group to capture the
                    // <value>
                preg_match_all("/--?[^=\s]+?=\"([^\"]+)\"?/", $worend, $matches);
                $val = $matches[1];
                $status = $val[0];
                $title = $val[1];

                $x++;
                    // Continue eating until we see the end indicator
                    // denoted by [END]. This is an extra precaution as
                    // it should always end with the last item
                    // in the array
                while (strpos($arr[$x], '[END]') === false) {
                    $message.= nl2br(" $arr[$x]\r\n");
                    $x++;
                }

                $message = str_replace("[END]", "", $message);
                    // We only care about the first returned
                    // error or success message. Break out early
                    // to avoid overwritting
                break;
            }
        }
    }

    if (isset($_POST["submit"])){
        display();
    }
    ?>

<!doctype html>
<html>
<head>
<base href="/~adeh6562/grade-notifier/Grade-Notifier/">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CUNY Grade Notifier</title>
<link type="text/css" rel="stylesheet" href="src/site/site-assets/css/styles.css">
<link href="https://fonts.googleapis.com/css?family=Roboto+Slab:400,700" rel="stylesheet">

<!-- Favicon and icons for other platforms -->
<link rel="apple-touch-icon" sizes="180x180" href="/src/site/site-assets/icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/src/site/site-assets/icons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/src/site/site-assets/icons/favicon-16x16.png">
<link rel="manifest" href="/src/site/site-assets/icons/site.webmanifest">
<link rel="mask-icon" href="/src/site/site-assets/icons/safari-pinned-tab.svg" color="#5bbad5">
<link rel="shortcut icon" href="/src/site/site-assets/icons/favicon.ico">
<meta name="apple-mobile-web-app-title" content="Grade Notifier">
<meta name="application-name" content="Grade Notifier">
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="msapplication-config" content="/src/site/site-assets/icons/browserconfig.xml">
<meta name="theme-color" content="#ffffff">
</head>
<body>
<div class="wrapper">
<div class="column column--left">
<?php
    if (!$landing):
    if ($status == "ok"):
    ?>
<img class="status-symbol" alt="Check" src="Assets/site/Check.svg">
<?php
    elseif ($status == "error"):
    ?>
<img class="status-symbol" alt="Exclamation mark" src="Assets/site/Exclamation.svg">
<?php
    endif;
    endif;
    ?>
<h1 class="callout">
<?php
    if ($landing):
    ?>
Get a text when you<br>get your grades!
<?php
    elseif ($title):
    echo $title;
    endif;
    ?>
</h1>
<?php
    if ($landing):
    ?>
<div class="callout__divider"></div>
<form action=<?php echo $_SERVER['PHP_SELF']; ?> method="POST">
<input class="input" type="text" name="username" placeholder="Username" required><span class="username-posttext">@login.cuny.edu</span>
<br>
<input class="input input--full-width" type="password" name="password" placeholder="Password" required>
<br>

<!-- <label for="school">School:</label> -->
<select class="input input--select input--full-width" id="school" name="school" required>
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
</select>
<br>

<input class="input input--full-width" type="text" name="phone" placeholder="Phone Number" required>
<br>
<input class="submit" type="submit" name="submit" value="Text me!">
</form>
<?php
    else:
    if($status == "ok"):
    ?>
<div class="confirm-message__wrapper">
<?php
    echo "<p class=\"confirm-message__text\">";
    echo htmlspecialchars($message);
    echo "</p>";
    ?>
</div>
<?php
    endif;

    if ($status == "error"):
    ?>
<form method="get">
<input class="submit" type="submit" value="Start over">
</form>
<?php
    endif;
    endif;
    ?>

<div class="credits">
<h3 class="credit">Made with ❤️  by Ehud Adler</h3>
<h4 class="credit">Big thanks to @ericshermancs</h4>
</div>
</div>

<div class="column column--right">
<?php
    if ($landing):
    ?>
<img class="image" alt="Phone" src="Assets/site/undraw_mobile_life_381t_edited.svg">
<?php
    elseif ($status == "ok"):
    ?>
<img class="image" alt="Phone with check mark" src="Assets/site/undraw_order_confirmed_1m3v.svg">
<?php
    elseif ($status == "error"):
    ?>
<img class="image" alt="Phone with exclamation mark" src="Assets/site/undraw_order_confirmed_1m3v_and_heartbroken_cble.svg">
<?php
    endif
    ?>
</div>
</div>
</body>
</html>

