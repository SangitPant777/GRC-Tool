// Check if the user has already been authenticated
const isAuthenticated = sessionStorage.getItem('authenticated');

// If the user is already authenticated, redirect to the dashboard
if (isAuthenticated) {
    window.location.href = "index.html"; // Replace "dashboard.html" with the filename of your dashboard HTML file
} else {
    // Define the correct password
    const correctPassword = "sangit";

    // Prompt the user to enter the password
    const enteredPassword = prompt("Please enter the password to access the dashboard:");

    // Check if the entered password is correct
    if (enteredPassword === correctPassword) {
        // Password is correct, set authentication flag and redirect to the dashboard
        sessionStorage.setItem('authenticated', true);
        window.location.href = "index.html"; // Replace "dashboard.html" with the filename of your dashboard HTML file
    } else {
        // Password is incorrect, show an error message and deny access
        alert("Incorrect password! Access denied.");
        window.location.href = "about:blank"; // Redirect to a blank page
    }
}
