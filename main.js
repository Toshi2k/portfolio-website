document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');

  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('open');
    });
  }

  const form = document.querySelector('#contact-form');
  const successMessage = document.querySelector('#form-success');

  if (form) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const name = form.querySelector('input[name="name"]').value.trim();
      const email = form.querySelector('input[name="email"]').value.trim();
      const message = form.querySelector('textarea[name="message"]').value.trim();

      if (!name || !email || !message) {
        successMessage.textContent = 'Please fill out all fields before sending.';
        successMessage.style.color = '#f7c0c0';
        return;
      }

      form.reset();
      successMessage.textContent = 'Thanks! Your message has been sent. I’ll respond soon.';
      successMessage.style.color = '#b5f1c2';
    });
  }
});