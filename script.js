// Floating CTA Bar - Always visible, sticky to header
const floatingCta = document.getElementById('floatingCta');
const header = document.querySelector('.header');

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

// Scroll animations disabled per user request
// All elements appear immediately without fade-in effects

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

// Function to change main interior image with smooth transition
function changeImage(element, imageSrc) {
    const mainImage = document.getElementById('mainInteriorImage');
    const thumbnails = document.querySelectorAll('.thumb-item');
    
    // Remove active class from all thumbnails
    thumbnails.forEach(thumb => thumb.classList.remove('active'));
    
    // Add active class to clicked thumbnail
    element.classList.add('active');
    
    // Fade out main image
    mainImage.style.opacity = '0';
    mainImage.style.transform = 'scale(0.95)';
    
    setTimeout(() => {
        // Change source and fade in
        mainImage.src = imageSrc;
        mainImage.style.opacity = '1';
        mainImage.style.transform = 'scale(1)';
    }, 300);
}

// Ensure main image transition is set
const mainInteriorImage = document.getElementById('mainInteriorImage');
if (mainInteriorImage) {
    mainInteriorImage.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
}

// Parallax effect for hero section
const hero = document.querySelector('.hero');
if (hero) {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxSpeed = 0.5;
        hero.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
    });
}

// Enhanced header scroll effect
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        header.style.boxShadow = '0 10px 30px -10px rgba(0, 0, 0, 0.1), 0 0 60px rgba(37, 99, 235, 0.08)';
        header.style.backdropFilter = 'blur(25px) saturate(200%)';
    } else {
        header.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
        header.style.backdropFilter = 'blur(20px) saturate(180%)';
    }
    
    lastScroll = currentScroll;
});

// Add hover effect enhancement for cards
const cards = document.querySelectorAll('.pricing-card, .spec-card, .testimonial-card');
cards.forEach(card => {
    card.addEventListener('mouseenter', function(e) {
        this.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.6, 1)';
    });
    
    card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        
        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-12px) scale(1.02)`;
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
    });
});

// Button ripple effect
const buttons = document.querySelectorAll('.btn');
buttons.forEach(button => {
    button.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            transform: translate(-50%, -50%) scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: translate(-50%, -50%) scale(20);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
