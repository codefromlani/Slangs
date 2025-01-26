
document.getElementById('submitForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    const submitButton = e.target.querySelector('button[type="submit"]');

    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';

    const abbreviation = document.getElementById('abbreviation').value;
    const meaning = document.getElementById('meaning').value;

    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    try {
        const response = await fetch('http://localhost:8000/abbreviations', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                abbreviation: abbreviation.trim(),
                meaning: meaning.trim()
            })
        });

        const data = await response.json();
        console.log('Response data:', data);

        if (!response.ok) {

            if (response.status === 409) {
                errorMessage.textContent = data.detail || 'Conflict error occurred, please try again.';
            } else {
                errorMessage.textContent = data.detail || 'Something went wrong. Please try again.';
            }
            errorMessage.style.display = 'block';
        } else {
         
            successMessage.textContent = data.message || 'Your slang was submitted successfully and is pending review!';
            successMessage.style.display = 'block';
    
            setTimeout(() => {
                successMessage.style.display = 'none'; 
                document.getElementById('submitForm').reset(); 
            }, 5000); 
        }
    } catch (error) {
        console.error('Error:', error);
        errorMessage.textContent = 'Network error. Please check your connection and try again.';
        errorMessage.style.display = 'block';
    } finally {
      
        submitButton.disabled = false;
        submitButton.textContent = 'Submit for Review';
    }
});

