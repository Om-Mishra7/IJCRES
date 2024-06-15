document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.insight .value');

    function animateCount(element, target) {
        let current = 0;
        const increment = target / 100;
        const duration = 2000; // 2 seconds
        const stepTime = duration / (target / increment);

        function updateCount() {
            current += increment;
            if (current < target) {
                element.textContent = Math.ceil(current) + ' days';
                requestAnimationFrame(updateCount);
            } else {
                element.textContent = target + ' days';
            }
        }

        updateCount();
    }

    const observerOptions = {
        threshold: 0.5 // Adjust based on when you want the animation to start
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const targetText = element.textContent;
                const targetNumber = parseInt(targetText.match(/\d+/)[0], 10);
                animateCount(element, targetNumber);
                observer.unobserve(element); // Stop observing once animation starts
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    elements.forEach(el => {
        observer.observe(el);
    });
});


// signup

// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}