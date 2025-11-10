// Theme Toggle Functionality
(function() {
    'use strict';
    
    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    // Get stored theme or default to light
    const getStoredTheme = () => localStorage.getItem('theme') || 'light';
    const setStoredTheme = theme => localStorage.setItem('theme', theme);
    
    // Set theme
    const setTheme = theme => {
        htmlElement.setAttribute('data-bs-theme', theme);
        updateIcon(theme);
        setStoredTheme(theme);
    };
    
    // Update icon based on theme
    const updateIcon = theme => {
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            }
        }
    };
    
    // Initialize theme on page load
    setTheme(getStoredTheme());
    
    // Toggle theme on button click
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            setTheme(newTheme);
        });
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
})();

// Form validation enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Add Bootstrap validation to forms
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // File upload preview
    const fileInput = document.getElementById('evidence');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileCount = this.files.length;
            const fileText = this.nextElementSibling;
            if (fileText && fileText.classList.contains('form-text')) {
                if (fileCount > 0) {
                    fileText.innerHTML = `<i class="fas fa-check-circle text-success me-1"></i>${fileCount} file(s) selected`;
                } else {
                    fileText.innerHTML = `<i class="fas fa-paperclip me-1"></i>You can upload multiple files (images or PDFs). Max size: 16MB per file.`;
                }
            }
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});