<!DOCTYPE html>
<html >
<head>
  <meta charset="UTF-8">
  <title>Recaptcha test zone</title>
    <link rel="stylesheet" href="css/style.css">
    <script src='https://www.google.com/recaptcha/api.js'></script>
</head>

<?php
ini_set("display_errors", 1);
ini_set("display_startup_errors", 1);
error_reporting(E_ALL);

// Test Key
// $site_Key = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI";
// $secret_Key = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe";
$site_Key = "6LfhymQUAAAAAOVG5FQtdIbEcw_ywvv_P841oYMb";
$secret_Key = "Tmt4bWFIbHRVVlZCUVVGQlFWQnFORWRGWm00MGJGRnZaMlkzTmxwRk4xWlRkVlZVT1dWYVZ3PT0=";
$ip = $_SERVER['REMOTE_ADDR'];

$success = "FALSE";

if(isset($_POST['message'])){
    $message = addslashes($_POST['message']);
}

if(isset($_POST['g-recaptcha-response'])){
    $g_recaptcha = addslashes($_POST['g-recaptcha-response']);

	$url = 'https://www.google.com/recaptcha/api/siteverify';
	$data = array(
		'secret' => base64_decode(base64_decode($secret_Key)),
		'response' => $g_recaptcha
	);
	$options = array(
		'http' => array (
            'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
			'method' => 'POST',
			'content' => http_build_query($data)
		)
    );
    
	$context  = stream_context_create($options);
	$response_data = file_get_contents($url, false, $context);
	$response=json_decode($response_data);
	if ($response->success==TRUE) {
        $success = "TRUE";
    }
}

?>

<body>
<div class="container">
  <div class="info">
    <h1>Google Recaptcha</h1><span>Test Zone</span>
  </div>
</div>
<div class="form">
  <!-- <div class="thumbnail"><img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/169963/hat.svg"/></div> -->
  <form class="login-form" action="./index.php" method="post">
        <!-- <div class="center" style="margin-bottom: 30px;">
            <select name="option" id="sources" class="custom-select sources" placeholder="이용수단">
                <option value="1">placeholder 1</option>
                <option value="2">placeholder 2</option>
            </select>
        </div> -->

    Site Key
    <input type="text" name="Site Key" value="6LfhymQUAAAAAOVG5FQtdIbEcw_ywvv_P841oYMb" readonly/>
    <br>
    <input type="text" name="message" placeholder="text1"/>
    <input type="text" name="g-recaptcha-response" placeholder="g-recaptcha-response"/>
    <div class="g-recaptcha" data-sitekey="6LfhymQUAAAAAOVG5FQtdIbEcw_ywvv_P841oYMb"></div>
    <br>
    <button>Submit</button>
    </form>
    <form action="#">
        <?php
        echo"<br>RECAPTCHA = $success<br>";
        if(isset($message)){
            echo"message = $message<br>";
        }else{
            echo"<br>NULL<br>";
        }
        if(isset($g_recaptcha)){
            echo"g-recaptcha-response = $g_recaptcha<br>";
        }else{
            echo"<br>NULL<br>";
        }
        ?>
    </form>
</div>
</body>
</html>
<!-- <style>
    body {
        background: #ededed;
        font-family: 'Open Sans', sans-serif;
    }
    .center {
        display: inline-block;
        top: 50%; left: 50%;
    }

    /** Custom Select **/
    .custom-select-wrapper {
        position: relative;
        display: inline-block;
        user-select: none;
    }
    .custom-select-wrapper select {
        display: none;
    }
    .custom-select {
        position: relative;
        display: inline-block;
    }
    .custom-select-trigger {
        position: relative;
        display: block;
        width: 130px;
        padding: 0 84px 0 22px;
        font-size: 22px;
        font-weight: 300;
        color: #fff;
        line-height: 60px;
        background: #EF3B3A;
        border-radius: 4px;
        cursor: pointer;
    }
    .custom-select-trigger:after {
        position: absolute;
        display: block;
        content: '';
        width: 10px; height: 10px;
        top: 50%; right: 25px;
        margin-top: -3px;
        border-bottom: 1px solid #fff;
        border-right: 1px solid #fff;
        transform: rotate(45deg) translateY(-50%);
        transition: all .4s ease-in-out;
        transform-origin: 50% 0;
    }
    .custom-select.opened .custom-select-trigger:after {
        margin-top: 3px;
        transform: rotate(-135deg) translateY(-50%);
    }
    .custom-options {
        position: absolute;
        display: block;
        top: 100%; left: 0; right: 0;
        min-width: 100%;
        margin: 15px 0;
        border: 1px solid #b5b5b5;
        border-radius: 4px;
        box-sizing: border-box;
        box-shadow: 0 2px 1px rgba(0,0,0,.07);
        background: #fff;
        transition: all .4s ease-in-out;

        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transform: translateY(-15px);
    }
    .custom-select.opened .custom-options {
        opacity: 1;
        visibility: visible;
        pointer-events: all;
        transform: translateY(0);
    }
    .custom-options:before {
        position: absolute;
        display: block;
        content: '';
        bottom: 100%; right: 25px;
        width: 7px; height: 7px;
        margin-bottom: -4px;
        border-top: 1px solid #b5b5b5;
        border-left: 1px solid #b5b5b5;
        background: #fff;
        transform: rotate(45deg);
        transition: all .4s ease-in-out;
    }
    .option-hover:before {
        background: #f9f9f9;
    }
    .custom-option {
        position: relative;
        display: block;
        padding: 0 22px;
        border-bottom: 1px solid #b5b5b5;
        font-size: 18px;
        font-weight: 600;
        color: #b5b5b5;
        line-height: 47px;
        cursor: pointer;
        transition: all .4s ease-in-out;
    }
    .custom-option:first-of-type {
        border-radius: 4px 4px 0 0;
    }
    .custom-option:last-of-type {
        border-bottom: 0;
        border-radius: 0 0 4px 4px;
    }
    .custom-option:hover,
    .custom-option.selection {
        background: #f9f9f9;
        color: #EF3B3A;
    }
</style> -->