#!/usr/local/bin/php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<div>
<?php
    if (isset($_GET['email']) && isset($_GET['token'])) {
        $file_unvalidated = @fopen("unvalidated.txt", 'r');

        if ($file_unvalidated) { // file can be open or created
            while(!feof($file_unvalidated)) { // read lines of file until no more to read
                $json_line = fgets($file_unvalidated);
                if ( empty(trim($json_line)) ) { // empty file means no account regresitered
                    break;
                }
                $line = json_decode($json_line, true); // convert array object
                if ($line['email'] === $_GET['email'] && $line['token'] === $_GET['token']) {
                    $contents = file_get_contents("unvalidated.txt");
                    $contents = str_replace($json_line, '', $contents);
                    file_put_contents("unvalidated.txt", $contents);

                    $file_validated = @fopen("validated.txt", 'a');

                    $user = array('email'=>$_GET['email'], 'password'=>$line['password']); // create an array object
                    $data = json_encode($user); // encode array into JSON object

                    fwrite($file_validated, $data); // write JSON object into the file
                    fwrite($file_validated, "\n"); // add next_line at the end of the file
                    echo "You are registered!<br/>";

                    fclose($file_validated);
                    
                    break;
                }
            }
            fclose($file_unvalidated);
        } else { // failed to open or create the file
            echo 'cannot open the file or the file is not exits!';
        }
    }
?>
</div> 
<footer>
    <small> &copy; <em id="date">2022</em> Harvey Cheng </small>
</footer>
</body>
</html>