// routes/web.php Route::post('/check-image', [ImageController::class, 'checkImage']);

// app/Http/Controllers/ImageController.php namespace App\Http\Controllers;

use Illuminate\Http\Request; use Illuminate\Support\Facades\Storage;

class ImageController extends Controller { public function checkImage(Request $request) { // Validate the request to ensure an image file is provided $request->validate([ 'image' => 'required|image', ]);

    // Store the uploaded image temporarily
    $image = $request->file('image');
    $imagePath = $image->storeAs('temp_images', $image->getClientOriginalName());

    // Define the command to execute the Python script
    $pythonScript = '/path/to/your_script.py';
    $command = escapeshellcmd("python3 $pythonScript " . storage_path('app/' . $imagePath));

    // Execute the command and capture the output
    $output = shell_exec($command);

    // Decode the JSON output
    $result = json_decode($output, true);

    // Check if the image is known and return the appropriate response
    if ($result['known']) {
        return response()->json([
            'message' => 'The image is already known.',
            'matched_image' => $result['img_name'],
            'similarity' => $result['similarity']
        ]);
    } else {
        return response()->json(['message' => 'The image is not known.']);
    }
}

}
