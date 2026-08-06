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

    // 4. Chatbot Widget (Groq-powered)
    const chatbotWidget = document.getElementById('chatbotWidget');
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotClose = document.getElementById('chatbotClose');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotForm = document.getElementById('chatbotForm');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotSend = document.getElementById('chatbotSend');

    if (chatbotWidget && chatbotForm) {
        function openChat() {
            chatbotWidget.classList.add('open');
            setTimeout(() => chatbotInput.focus(), 300);
        }

        function closeChat() {
            chatbotWidget.classList.remove('open');
        }

        chatbotToggle.addEventListener('click', openChat);
        chatbotClose.addEventListener('click', closeChat);

        function appendMessage(role, text) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('chat-message', role);
            const p = document.createElement('p');
            p.textContent = text;
            messageDiv.appendChild(p);
            chatbotMessages.appendChild(messageDiv);
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }

        function setSending(isSending) {
            chatbotSend.disabled = isSending;
            chatbotInput.disabled = isSending;
            chatbotSend.textContent = isSending ? '...' : 'Send';
        }

        chatbotForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatbotInput.value.trim();
            if (!message) return;

            appendMessage('user', message);
            chatbotInput.value = '';
            setSending(true);

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });

                const result = await response.json();

                if (response.ok && result.status === 'success') {
                    appendMessage('bot', result.reply);
                } else {
                    appendMessage('bot', result.message || 'Sorry, something went wrong. Please try again.');
                }
            } catch (err) {
                console.error('Chat Error:', err);
                appendMessage('bot', 'Failed to connect to the server. Please try again later.');
            } finally {
                setSending(false);
                chatbotInput.focus();
            }
        });
    }
});
