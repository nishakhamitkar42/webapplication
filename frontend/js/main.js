document.addEventListener('DOMContentLoaded', () => {
    // 1. Skill Bar Animations
    // Animate the progress bars when visiting the Skills page
    const skillBars = document.querySelectorAll('.skill-bar-fill');
    if (skillBars.length > 0) {
        // Delay slightly for visual effect after page load
        setTimeout(() => {
            skillBars.forEach(bar => {
                const targetPercent = bar.getAttribute('data-percent');
                bar.style.width = `${targetPercent}%`;
            });
        }, 300);
    }

    // 2. Interactive Navigation Active Highlights
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links li');
    
    navLinks.forEach(link => {
        const anchor = link.querySelector('a');
        if (anchor) {
            const href = anchor.getAttribute('href');
            if (href === currentPath || (currentPath === '/' && href === '/')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        }
    });

    // 3. Contact Form Submission via AJAX (REST API)
    const contactForm = document.getElementById('contactForm');
    const alertBox = document.getElementById('alertBox');
    const alertMessage = document.getElementById('alertMessage');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('spinner');

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Hide previous alerts
            alertBox.style.display = 'none';
            alertBox.className = 'alert-box';

            // Gather values
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();

            // Client-side Validation
            if (!name || !email || !subject || !message) {
                showAlert('All fields are required.', 'danger');
                return;
            }

            const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;
            if (!emailRegex.test(email)) {
                showAlert('Please enter a valid email address.', 'danger');
                return;
            }

            // Set UI Loading State
            setLoadingState(true);

            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name, email, subject, message })
                });

                const result = await response.json();

                if (response.ok && result.status === 'success') {
                    showAlert(result.message, 'success');
                    contactForm.reset();
                } else {
                    showAlert(result.message || 'An error occurred during submission.', 'danger');
                }
            } catch (err) {
                console.error('Submission Error:', err);
                showAlert('Failed to connect to the server. Please try again later.', 'danger');
            } finally {
                setLoadingState(false);
            }
        });
    }

    // Helper functions for alerts and loader
    function showAlert(msg, type) {
        alertMessage.textContent = msg;
        alertBox.style.display = 'flex';
        if (type === 'success') {
            alertBox.classList.add('alert-success');
        } else {
            alertBox.classList.add('alert-danger');
        }
        // Scroll to alert
        alertBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.textContent = 'Sending Message...';
            spinner.style.display = 'block';
        } else {
            submitBtn.disabled = false;
            btnText.textContent = 'Send Message';
            spinner.style.display = 'none';
        }
    }
});
