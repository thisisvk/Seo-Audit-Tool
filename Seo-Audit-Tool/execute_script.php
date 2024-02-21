<?php

// Validate and sanitize the URL input
$url = isset($_POST['url']) ? filter_var($_POST['url'], FILTER_SANITIZE_URL) : '';
if (empty($url)) {
    die("Invalid URL");
}

// Execute the Python script with the URL as an argument
$command = "python3 main.py " . escapeshellarg($url);
exec($command, $output, $return_var);

// Check if the script executed successfully
if ($return_var === 0) {
    // Script executed successfully, do something with the output if needed
    foreach ($output as $line) {
        echo $line . "<br>";
    }
} else {
    // Script execution failed
    echo "An error occurred while executing the script.";
}

?>
