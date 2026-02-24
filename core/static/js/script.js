// ============================================
// MAIN SCRIPT — Premium Skill Exchange Network
// ============================================
//
// This file handles all the interactive JavaScript features:
//   1. Animated counters (live stats on the home page)
//   2. Smooth scroll and parallax effects
//   3. Navbar shrink on scroll
//   4. Form submit button loading state
//   5. Floating particles in the hero section
//   6. Bootstrap tooltips initialization
//   7. Custom notification system (toast-style alerts)
//
// Dependencies: Bootstrap 5 (for tooltips)
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Premium Skill Exchange Network Loaded');

    // Initialize all features when the page is ready
    initializeCounters();
    initializeAnimations();
    initializeFormValidation();
    initializeNavbar();
    initializeParticles();
    initializeTooltips();
});


// ============================================
// LIVE COUNTERS WITH ANIMATION
// ============================================
// Makes numbers count up from 0 to their target value
// when they scroll into view. Uses IntersectionObserver
// to detect when counters become visible.

function initializeCounters() {
    const counters = document.querySelectorAll('.live-counter, .stat-number');

    const animateCounter = (element) => {
        const target = parseInt(element.textContent) || 0;
        const duration = 2000; // 2 seconds for the animation
        const start = 0;
        const startTime = Date.now();

        const updateCounter = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // easeOutQuart — starts fast, slows down at the end
            // This makes the counter feel natural (not linear)
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(start + (target - start) * easeOutQuart);

            element.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(updateCounter); // Keep animating
            } else {
                element.textContent = target; // Ensure we end on the exact number
            }
        };

        updateCounter();
    };

    // Only animate when the counter scrolls into view (not on page load)
    // threshold: 0.5 means "trigger when 50% of the element is visible"
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                animateCounter(entry.target);
                entry.target.dataset.animated = 'true'; // Prevent re-animation
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}


// ============================================
// ANIMATIONS — Smooth Scroll & Parallax
// ============================================

function initializeAnimations() {
    // Smooth scrolling for anchor links (e.g., href="#features")
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Parallax effect — decorative shapes follow the mouse cursor
    // Each shape moves at a different speed based on its index,
    // creating a depth illusion (parallax)
    const shapes = document.querySelectorAll('.shape');
    if (shapes.length > 0) {
        let ticking = false; // Throttle flag to prevent excessive repaints

        document.addEventListener('mousemove', (e) => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const mouseX = e.clientX / window.innerWidth;   // 0 to 1
                    const mouseY = e.clientY / window.innerHeight;  // 0 to 1

                    shapes.forEach((shape, index) => {
                        // Higher index = faster movement = feels "closer"
                        const speed = (index + 1) * 0.02;
                        const x = mouseX * speed * 100;
                        const y = mouseY * speed * 100;

                        shape.style.transform = `translate(${x}px, ${y}px)`;
                    });

                    ticking = false;
                });

                ticking = true;
            }
        });
    }
}


// ============================================
// NAVBAR — Shrink on Scroll
// ============================================
// Adds a 'scrolled' class to the navbar when the user scrolls
// past 50px. CSS uses this class to make the navbar more compact.

function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
}


// ============================================
// FORM VALIDATION — Submit Button Loading State
// ============================================
// When a form is submitted, replaces the button text with a
// spinning icon and disables it to prevent double-submission.
// Re-enables after 5 seconds as a safety fallback.

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;

                // Fallback: re-enable button after 5 seconds
                // in case the form submission takes too long or fails
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}


// ============================================
// PARTICLES EFFECT — Floating Dots in Hero
// ============================================
// Creates 30 small floating circles in the hero section
// for a dynamic, modern background effect.

function initializeParticles() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    // Create a container for particles (pointer-events: none so they don't
    // interfere with clicking buttons/links)
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    particlesContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
        z-index: 1;
    `;

    heroSection.appendChild(particlesContainer);

    // Generate 30 particles with random sizes, positions, and animation timing
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: float ${Math.random() * 10 + 10}s linear infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        particlesContainer.appendChild(particle);
    }
}


// ============================================
// TOOLTIPS — Bootstrap Tooltip Initialization
// ============================================
// Finds all elements with data-bs-toggle="tooltip"
// and initializes Bootstrap's tooltip component on them.

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );

    // Only initialize if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}


// ============================================
// NOTIFICATION SYSTEM — Custom Toast Alerts
// ============================================
// Creates toast-style notifications that slide in from the right.
// Used for AJAX success/error messages.
//
// Usage: showNotification('Request sent!', 'success');
// Types: 'success', 'error', 'warning', 'info'

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `premium-notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)} me-2"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    document.body.appendChild(notification);

    // Slide in after a tiny delay (so the CSS transition actually triggers)
    setTimeout(() => notification.classList.add('show'), 10);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300); // Wait for slide-out animation
    }, 5000);
}

// Map notification types to Font Awesome icons
function getNotificationIcon(type) {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return icons[type] || icons.info;
}


// ============================================
// UTILITY — CSRF Cookie Reader
// ============================================
// Reads Django's CSRF token from cookies.
// Needed for AJAX POST requests to pass CSRF validation.

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie starts with the name we're looking for
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// ============================================
// INJECT NOTIFICATION STYLES
// ============================================
// These styles are injected via JS because the notification
// system is self-contained (doesn't depend on external CSS).

const customStyles = document.createElement('style');
customStyles.textContent = `
    /* Toast notification — slides in from the right */
    .premium-notification {
        position: fixed;
        top: 100px;
        right: -400px;
        min-width: 350px;
        max-width: 450px;
        padding: 1.2rem 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        z-index: 9999;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-left: 4px solid #667eea;
    }

    .premium-notification.show {
        right: 20px; /* Slide into view */
    }

    /* Color variants — colored left border indicates type */
    .premium-notification.success {
        border-left-color: #4facfe;
    }

    .premium-notification.error {
        border-left-color: #fa709a;
    }

    .premium-notification.warning {
        border-left-color: #fee140;
    }

    .notification-content {
        display: flex;
        align-items: center;
        color: #2d3748;
        font-weight: 600;
        flex: 1;
    }

    .notification-close {
        background: none;
        border: none;
        color: #2d3748;
        opacity: 0.5;
        cursor: pointer;
        padding: 0.5rem;
        transition: opacity 0.2s;
    }

    .notification-close:hover {
        opacity: 1;
    }

    /* Float animation for particles */
    @keyframes float {
        0%, 100% {
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        10%, 90% {
            opacity: 1;
        }
        50% {
            transform: translateY(-100vh) translateX(50px);
        }
    }
`;

document.head.appendChild(customStyles);

console.log('✅ Premium script loaded successfully');
