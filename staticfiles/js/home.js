document.addEventListener('DOMContentLoaded', function() {
    const heading = document.querySelector('h1');
    
    // fade-in animation
    heading.style.opacity = 0;
    heading.style.transition = 'opacity 1s ease-in-out';
    
    setTimeout(function() {
        heading.style.opacity = 1;
    }, 300);
});