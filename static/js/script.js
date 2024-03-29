document.getElementById('imageUpload').addEventListener('change', function(e) {
    var files = e.target.files;
    var imageDisplay = document.getElementById('imageDisplay');

    // Clear the image display area
    imageDisplay.innerHTML = '';

    for (var i = 0; i < files.length; i++) {
        var img = document.createElement('img');
        img.src = URL.createObjectURL(files[i]);
        img.onload = function() {
            URL.revokeObjectURL(this.src);
        }
        imageDisplay.appendChild(img);
    }
});