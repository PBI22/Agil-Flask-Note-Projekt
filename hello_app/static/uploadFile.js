async function uploadFile() {
  const fileInput = document.querySelector('input[type="file"]');
  const files = fileInput.files;
  const filenames = []; // Array to store filenames
  
  // Extract filenames from file input
  for (let i = 0; i < files.length; i++) {
    filenames.push(files[i].name);
  }
  
  const formData = new FormData();
  
  // Append files and filenames to FormData
  for (let i = 0; i < files.length; i++) {
    formData.append('file', files[i]);
    formData.append('filenames', filenames[i]); // Append filenames
  }
  
  try {
    const response = await fetch('/upload', {
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


// Function to upload files to final container
async function uploadFinalFile() {
  const fileInput = document.querySelector('input[type="file"]');
  const files = fileInput.files;
  const filenames = []; // Array to store filenames
  
  // Extract filenames from file input
  for (let i = 0; i < files.length; i++) {
    filenames.push(files[i].name);
  }
  
  const formData = new FormData();
  
  // Append files and filenames to FormData
  for (let i = 0; i < files.length; i++) {
    formData.append('file', files[i]);
    formData.append('filename', filenames[i]); // Append filenames
  }
  
  try {
    const response = await fetch('/uploadfiles', {
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

  


document.getElementById('submitForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Prevent the default form submission
  
  // Call the uploadFinalFile function to handle file uploads
  await uploadFinalFile();
  
  // Submit the form
  this.submit();
});