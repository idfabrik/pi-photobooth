<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>pi photobooth</title>
    <style>
        body { font-family: sans-serif; }
        .image-block { margin-bottom: 20px; }
        img { max-width: 300px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>cab4</h1>

    <?php
    $images = glob("*.jpg");
    usort($images, function($a, $b) {
        return filemtime($b) - filemtime($a);
    });

    foreach ($images as $image) {
        echo "<div class='image-block'>";
        echo "<a href='$image'><img src='$image' alt='$image'></a><br>";
        echo "<small>$image</small>";
        echo "</div>";
    }
    ?>
</body>
</html>