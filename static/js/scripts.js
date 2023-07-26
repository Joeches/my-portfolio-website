// Smooth scrolling for anchor links
document.querySelectorAll('nav a').forEach(link => {
  link.addEventListener('click', function (event) {
    event.preventDefault();
    const targetId = link.getAttribute('href');
    const target = document.querySelector(targetId);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Show/hide the navigation bar on scroll
let prevScrollPos = window.pageYOffset;
window.addEventListener('scroll', function () {
  const header = document.querySelector('header');
  const currentScrollPos = window.pageYOffset;
  if (prevScrollPos > currentScrollPos) {
    header.style.top = '0';
  } else {
    header.style.top = '-80px';
  }
  prevScrollPos = currentScrollPos;
});

// Toggle mobile menu
const toggleBtn = document.querySelector('.toggle-btn');
const navLinks = document.querySelector('nav ul');

toggleBtn.addEventListener('click', function () {
  navLinks.classList.toggle('show');
});

// Toggle "About Me" section visibility
const aboutContent = document.getElementById('about-content');
const aboutToggleButton = document.getElementById('toggle-button');

aboutContent.style.display = 'none'; // Hide the "About Me" content initially

aboutToggleButton.addEventListener('click', function () {
  if (aboutContent.style.display === 'none') {
    aboutContent.style.display = 'block';
    aboutToggleButton.textContent = 'Show Less';
  } else {
    aboutContent.style.display = 'none';
    aboutToggleButton.textContent = 'Show More';
  }
});


// Form submission using FormSubmit link
document.getElementById('contact-form').addEventListener('submit', function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);

  // Construct the FormSubmit link with the contact form data
  const formSubmitUrl = 'https://formsubmit.co/joechesmusic@gemail.com'; // Replace with your FormSubmit URL
  fetch(formSubmitUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(Object.fromEntries(formData.entries()))
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Show success message
      alert('Message sent successfully!');
    } else {
      // Show error message
      alert('Failed to send message. Please try again later.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
  });
});