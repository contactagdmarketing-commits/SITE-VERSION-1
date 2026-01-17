// Floating CTA Bar
const floatingCta = document.getElementById('floatingCta');
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        floatingCta.classList.add('show');
    } else {
        floatingCta.classList.remove('show');
    }
});

// Mobile Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });
}

// Close menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        menuToggle.classList.remove('active');
    });
});

// Exam Tabs Functionality
const examTabs = document.querySelectorAll('.exam-tab');
const examPanels = document.querySelectorAll('.exam-panel');

if (examTabs.length > 0) {
    examTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            
            // Remove active class from all tabs and panels
            examTabs.forEach(t => t.classList.remove('active'));
            examPanels.forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding panel
            tab.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Form Submission
const inscriptionForm = document.getElementById('inscriptionForm');

if (inscriptionForm) {
    inscriptionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(inscriptionForm);
        const data = Object.fromEntries(formData);
        
        // Basic validation
        if (!data.rgpd || !data.cgu) {
            alert('Veuillez accepter les conditions d\'utilisation et la politique de confidentialité.');
            return;
        }
        
        // Here you would normally send the data to a server
        // For now, we'll just show a success message
        alert('Votre demande a été envoyée avec succès ! Nous vous recontacterons sous 24-48h.');
        
        // Reset form
        inscriptionForm.reset();
        
        // In a real application, you would send the data to your backend:
        // fetch('/api/inscription', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(data)
        // })
        // .then(response => response.json())
        // .then(data => {
        //     alert('Votre demande a été envoyée avec succès !');
        //     inscriptionForm.reset();
        // })
        // .catch(error => {
        //     alert('Une erreur est survenue. Veuillez réessayer.');
        // });
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation on scroll (optional enhancement)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.pricing-card, .testimonial-card, .concept-block, .stat-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Animated counter for stats
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };

    updateCounter();
}

// Observe stat numbers for counter animation
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounter(entry.target);
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-number').forEach(stat => {
    statsObserver.observe(stat);
});
