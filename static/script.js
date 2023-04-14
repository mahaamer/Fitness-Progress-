// Get form elements
const form = document.querySelector("form");
const firstNameInput = document.querySelector("#first-name");
const lastNameInput = document.querySelector("#last-name");

// Get content elements
const content = document.querySelector(".content");
const welcomeDiv = document.querySelector(".welcome");
const fullNameSpan = document.querySelector(".full-name");
const dateSpan = document.querySelector(".date");
const signOutBtn = document.querySelector(".btn-danger");

// Check if first and last name are already stored in local storage
if (localStorage.getItem("firstName") && localStorage.getItem("lastName")) {
  // Update welcome message with full name and date
  const fullName = `${localStorage.getItem("firstName")} ${localStorage.getItem(
    "lastName"
  )}`;
  fullNameSpan.textContent = fullName;
  const currentDate = new Date().toLocaleDateString();
  dateSpan.textContent = currentDate;

  // Hide login form and show content div
  form.style.display = "none";
  content.style.display = "block";

  // Display welcome back message with date
  welcomeDiv.textContent = `Welcome back, ${fullName}! Today is ${currentDate}.`;
}

// Listen to form submit event
form.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent form submission

  // Store first and last name in local storage
  localStorage.setItem("firstName", firstNameInput.value);
  localStorage.setItem("lastName", lastNameInput.value);

  // Hide login form and show content div
  form.style.display = "none";
  content.style.display = "block";

  // Update welcome message with full name and date
  const fullName = `${localStorage.getItem("firstName")} ${localStorage.getItem(
    "lastName"
  )}`;
  fullNameSpan.textContent = fullName;
  const currentDate = new Date().toLocaleDateString();
  dateSpan.textContent = currentDate;

  // Display welcome message
  welcomeDiv.textContent = `Welcome, ${fullName}! Today is ${currentDate}.`;
});

// Listen to sign out button click event
signOutBtn.addEventListener("click", (event) => {
  // Clear local storage
  localStorage.removeItem("firstName");
  localStorage.removeItem("lastName");

  // Hide content div and show login form
  content.style.display = "none";
  form.style.display = "block";
});
