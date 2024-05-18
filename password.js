// Check if the user has already been authenticated
const isAuthenticated = sessionStorage.getItem('authenticated');

// If the user is already authenticated, redirect to the dashboard
if (isAuthenticated) {
    window.location.href = "index.html"; // Redirect to the dashboard
} else {
    // Define the correct password
    const correctPassword = "sangit";

    // Create an input field for the user to enter the password
    const passwordInput = document.createElement('input');
    passwordInput.type = 'password';
    passwordInput.placeholder = 'Enter the password';
    
    // Create a submit button
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';

    // Append the input field and submit button to a container element
    const container = document.createElement('div');
    container.appendChild(passwordInput);
    container.appendChild(submitButton);

    // Append the container to the body
    document.body.appendChild(container);

    // Add event listener to the submit button
    submitButton.addEventListener('click', function() {
        // Get the entered password
        const enteredPassword = passwordInput.value;

        // Check if the entered password is correct
        if (enteredPassword === correctPassword) {
            // Password is correct, set authentication flag and redirect to the dashboard
            sessionStorage.setItem('authenticated', true);
            window.location.href = "index.html"; // Redirect to the dashboard
        } else {
            // Password is incorrect, show an error message and deny access
            alert("Incorrect password! Access denied.");
            // Clear the input field
            passwordInput.value = '';
        }
    });
}
