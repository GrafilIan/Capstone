document.addEventListener('DOMContentLoaded', function() {
  const imagePreview = document.getElementById('profile_image_preview');
  const profileImageInput = document.getElementById('profile_image');

  profileImageInput.addEventListener('change', function(event) {

    const selectedImage = event.target.files[0];

    if (selectedImage) {
      const reader = new FileReader();

      reader.onload = function() {
        imagePreview.src = reader.result;
      };

      reader.readAsDataURL(selectedImage);
    } else {
      imagePreview.src = '#';
    }
  });
});
