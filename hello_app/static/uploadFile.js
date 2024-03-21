// Function to upload files
async function uploadFile() {
  const fileInput = document.querySelector('input[type="file"]');
  const files = fileInput.files;
  const formData = new FormData();
  
  for (let i = 0; i < files.length; i++) {
    formData.append('file', files[i]);
    formData.append('filenames', files[i].name); // Append filenames
  }
  
  try {
    const response = await fetch('/dam/upload', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      alert('Files uploaded successfully!');
      
      // Get the JSON response containing file links
      const data = await response.json();
      
      // Update the view to show the uploaded images
      const imageContainer = document.getElementById('imageContainer');
      imageContainer.innerHTML = '';
      data.file_links.forEach(link => {
        const img = document.createElement('img');
        img.src = link;
        img.alt = `!(${link})`;
        img.classList.add('note-img');
        imageContainer.appendChild(img);
      });
    } else {
      alert('Failed to upload files. Please try again.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An unexpected error occurred. Please try again later.');
  }
}

// Function to upload files
async function uploadFinalFile() {
  const fileInput = document.querySelector('input[type="file"]');
  const files = fileInput.files;
  const formData = new FormData();
  
  for (let i = 0; i < files.length; i++) {
    formData.append('file', files[i]);
    formData.append('filename', files[i].name); // Append filenames
  }
  
  try {
    const response = await fetch('/dam/uploadfiles', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      alert('Files uploaded successfully!');
      fileInput.value = ''; // Clear file input field
    } else {
      alert('Failed to upload files. Please try again.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An unexpected error occurred. Please try again later.');
  }
}

function handleDragDrop(event) {
  event.stopPropagation();
  event.preventDefault();

  // Retrieving the image source URL
  var imageUrl = event.dataTransfer.getData("URL");

  // Replace 'tempimages' with 'images' in the URL
  var modifiedImageUrl = imageUrl.replace("tempimages", "images");

  // Format the modified image URL for markdown
  const formattedImageUrl = `![480px-img](${modifiedImageUrl})`;

  // Append the formatted image URL to the text area
  document.getElementById("note").value += formattedImageUrl;
}

document.getElementById('submitForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Prevent the default form submission
  
  // Call the uploadFinalFile function to handle file uploads
  await uploadFinalFile();
  
  // Submit the form
  this.submit();
});
