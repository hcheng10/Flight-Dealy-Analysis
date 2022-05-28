#!/usr/local/bin/php
<?php
    ob_start();
    if (!file_exists(dirname(realpath(__FILE__)) . '/sessions/')) { // make seeeions folder if not exits
        mkdir(dirname(realpath(__FILE__)) . '/sessions/', 0777, true);
    }

    session_save_path(dirname(realpath(__FILE__)) . '/sessions/');
    session_name('login_status'); // name the session
    session_start(); // start a session

    if (!$_SESSION['loggedin']) { // this will return warning message if $_SESSION['loggedin'] first create
        $_SESSION['loggedin'] = false; // have not logged in
    }

    if (!$_SESSION['email']) { // this will return warning message if $_SESSION['email'] first create
        $_SESSION['email'] = null; // have not logged in, so no email recorded
    }

    /**
     * This function validates a passwords and set the $_SESSION token to true 
     * if it is correct, logging them in and sending them to the welcome page.
     * Otherwise it flags $valided as false.
     * 
     * @param string $password the password that user entered
     * @param boolean $valided the valided flag to possibly change
     */
    function validate($email, $password) {
        $file = @fopen("validated.txt", 'r');
        $matched = null;
        if ($file) { // file can be open or created
            while(!feof($file)) { // read lines of file until no more to read
                $json_line = fgets($file);
                if ( empty(trim($json_line)) ) { // empty file
                    break;
                }
                $line = json_decode($json_line, true); // convert array object
                if ($line['email'] === $email) { // check if the input email inside the opened file
                    $matched = $line;
                    break;
                }
            }

            fclose($file);

            if ($matched !== null) { // find a matched email
                $hashed_password = hash('md5', $password);
                if ($matched["password"] == $hashed_password) { // password match
                    $_SESSION['loggedin'] = true;
                    $_SESSION['email'] = $email;
                    header('Location: welcome.php');
                } else { // password not match
                    echo 'Your password is invaild.<br/>';
                }
            } else { // didnt find a matched email
                echo 'No such email address. Please register or validate.<br/>';
            }
        } else { // failed to open or create the file
            echo 'cannot open the file or the file is not exits!';
        }
    }

    /**
     * This function will register new account for user with valid email and password
     * and then send validation url to the input eamil. The user's email and hashed
     * password will be saved into unvalidated.txt file. 
     * 
     * @param string $email the email that user entered
     * @param string $password the password that user entered
     */
    function registeration($email, $password) {
        $file_validated = @fopen("validated.txt", 'r');
        $exits = false;
        if ($file_validated) { // file can be open or created
            while(!feof($file_validated)) { // read lines of file until no more to read
                $json_line = fgets($file_validated);
                if ( empty(trim($json_line)) ) { // empty file means no account regresitered
                    break;
                }
                $line = json_decode($json_line, true); // convert array object
                if ($line['email'] === $email) { // check if the input email inside the opened file
                    echo "Already registered. please log in!<br/>";
                    $exits = true;
                    break;
                }
            }
            fclose($file_validated);
        } else { // failed to open or create the file
            echo 'cannot open the file or the file is not exits!';
        }
        
        if (!$exits) { // if didnt find email in validated.txt, check unvalidated.txt
            $file_unvalidated = @fopen("unvalidated.txt", 'r');
            if ($file_unvalidated) { // file can be open or created
                while(!feof($file_unvalidated)) { // read lines of file until no more to read
                    $json_line = fgets($file_unvalidated);
                    if ( empty(trim($json_line)) ) { // empty file means no account regresitered
                        break;
                    }
                    $line = json_decode($json_line, true); // convert array object
                    if ($line['email'] === $email) { // check if the input email inside the opened file
                        echo "Already regisetered, please go to your email to validate!.<br/>";
                        $exits = true;
                        break;
                    }
                }
                fclose($file_unvalidated);
            } else { // failed to open or create the file
                echo 'cannot open the file or the file is not exits!';
            }
        }

        if (!$exits) {
            $file = @fopen("unvalidated.txt", 'a');
            $hashed_password = hash('md5', $password); // hash password
            $token = mt_rand(100, 50000);
            $token = hash('md5', $token);
            $user = array('email'=>$email, 'password'=>$hashed_password, 'token'=>$token); // create an array object
            $data = json_encode($user); // encode array into JSON object

            fwrite($file, $data); // write JSON object into the file
            fwrite($file, "\n"); // add next_line at the end of the file
            echo "A validation email has been sent to: ", $email, ". Please follow the link.<br/>";

            $validation_url = "https://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]"; // get current url
            $validation_url = str_replace("index.php", "validate.php", $validation_url);
            $validation_url = $validation_url . "?email=" . $email . "&token=" . $token;
            $message = "Validate by clicking here: " . $validation_url;

            mail($email, 'validation', $message);
            
            fclose($file);
        }
    }

    if ($_SESSION['loggedin'] == true) {
        header('Location: welcome.php');
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login Page</title>
    </head>

<body>
<mian>
    <fieldset>
    <form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
        <label for="email">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Email:</label>
        <input id="email" type="email" name="email" pattern=".*[a-zA-Z]+.*@.*[a-zA-Z]+.*" required/><br/> 
        <!--standard email: [a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$-->
        <label for="password">Password:</label>
        <input id="password" type="password" name="password" pattern="[a-zA-Z0-9]{6,}" required/><br/>

        <input id="register" name="register" type="submit" value="register"/>
        <input id="login" name="login" type="submit" value="log in"/><br/>
    </form>
    </fieldset>
    <div>
        <?php
            if (isset($_POST["register"])) {
                registeration($_POST["email"], $_POST["password"]);
            }
            if (isset($_POST["login"])) {
                validate($_POST["email"], $_POST["password"]);
            }
        ?>
    </div>
</mian>

<footer>
    <br/><small>&copy; <em id="date"> 2022 </em> Harvey Cheng </small>
</footer>    
</body>
</html>