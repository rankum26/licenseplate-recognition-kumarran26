document.addEventListener("DOMContentLoaded", function() {
    const input = document.querySelector('input[type="file"]');
    const preview = document.createElement('img');
    preview.classList.add('preview');
    input.parentNode.insertBefore(preview, input.nextSibling);

    input.addEventListener('change', function() {
        const file = input.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            preview.src = e.target.result;
        }

        if (file) {
            reader.readAsDataURL(file);
        } else {
            preview.src = "";
        }
    });
});
