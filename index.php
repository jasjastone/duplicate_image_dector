$pythonScript = '/path/to/your_script.py';
$command = escapeshellcmd("python3 $pythonScript " . storage_path('app/' . $imagePath));

// Execute the command and capture the output
$output = shell_exec($command);

// Decode the JSON output from python script
$result = json_decode($output, true);
