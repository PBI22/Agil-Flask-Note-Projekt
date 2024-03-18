// Function to upload files
async function uploadFile() {
    // Get the file input element
    const fileInput = document.querySelector('input[type="file"]');
    
    // Get the files selected by the user
    const files = fileInput.files;
    
    // Create a FormData object to send the files to the server
    const formData = new FormData();
    
    // Append each file to the FormData object
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }
    
    try {
      // Send a POST request to the server with the FormData containing the files
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });
      
      // Check if the request was successful
      if (response.ok) {
        // Display a success message to the user
        alert('Files uploaded successfully!');
        
        // Clear the file input field
        fileInput.value = '';
        
        // Parse the JSON response
        const data = await response.json();
        
        // Update the view to show the uploaded images
        const imageContainer = document.getElementById('imageContainer');
        imageContainer.innerHTML = '';
        data.file_links.forEach(link => {
          const img = document.createElement('img');
          img.src = link;
          img.alt = `!(${link})`
          img.classList.add('note-img');
          imageContainer.appendChild(img);
        });
      } else {
        // Display an error message to the user
        alert('Failed to upload files. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      // Display an error message to the user
      alert('An unexpected error occurred. Please try again later.');
    }
  }
  