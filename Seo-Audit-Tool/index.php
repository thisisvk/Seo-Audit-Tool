<?php

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the URL input from the form
    $url = $_POST["url"];

    // Execute the Python script with the URL as a command-line argument
    $command = "C:/Users/test/AppData/Local/Programs/Python/Python312/python.exe main.py " . escapeshellarg($url);
    
    // Debugging: Print the command being executed
    echo "Executing command: $command<br>";

    // Execute the command and capture the output and return value
    exec($command, $output, $return_var);

    // Check if the Python script executed successfully
    if ($return_var === 0) {
        // Python script executed successfully, output the results
        foreach ($output as $line) {
            echo $line . "<br>";
        }
    } else {
        // Python script execution failed, output an error message
        echo "An error occurred while executing the Python script.<br>";
        // Debugging: Print the return value
        echo "Return value: $return_var<br>";
        // Debugging: Print the output
        echo "Output:<br>";
        var_dump($output);
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SEO Audit Tool</title>
</head>
<body>
    <h1>SEO Audit Tool</h1>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
        <label for="url">Enter URL:</label>
        <input type="text" name="url" id="url" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
