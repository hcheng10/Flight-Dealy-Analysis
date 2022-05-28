#!/usr/local/bin/php
<?php
    ob_start();
    session_save_path(dirname(realpath(__FILE__)) . '/sessions/');
    session_name('login_status');
    session_start(); // start a session
?>
<!DOCTYPE html>
<html lang="en">
<?php if (!isset($_SESSION['loggedin']) or !$_SESSION['loggedin']) { ?>
    <head>
    <meta charset="UTF-8">
    <title>Unwelcome!</title>
    </head> 
    <body>
    <p>Go back and log in.</p>
<?php } else { ?>
    <head>
    <meta charset="UTF-8">
    <title>Welcome!</title>
    </head>
    <body>
    <p>
        Welcome! Your email address is: <?php echo $_SESSION['email']; ?><br/>
        Here is a list of all regrestered addresses:
    </p>
    <div>
<?php
    $file = @fopen("validated.txt", 'r');
    if ($file) { // file can be open or created
        while(!feof($file)) { // read lines of file until no more to read
            $json_line = fgets($file);
            // if ( empty(trim($json_line)) ) { // empty file or last line
            //     break;
            // }
            $line = json_decode($json_line, true); // convert array object
            echo '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', $line["email"], '<br/>';
        }

        fclose($file);
    } else { // failed to open or create the file
        echo 'cannot open the file or the file is not exits!';
    } ?>
    </div>
    <br/>
    <form method="post">
        <input id="logout" name="logout" type="submit" value="log out"/>
    </form>
<?php
} ?>
<footer>
    <br/><small>&copy; <em id="date"> 2022 </em> Harvey Cheng </small>
</footer>    
</body>
</html>
<?php 
    if (isset($_POST["logout"])) {
        $_SESSION['loggedin'] = false; // have not logged in
        $_SESSION['email'] = null; // have not logged in, so no email recorded
        header('Location: index.php');
    }
?>