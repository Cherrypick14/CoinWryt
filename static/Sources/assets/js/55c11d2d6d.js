// lazyload.js
document.addEventListener("DOMContentLoaded", function () {
  const lazyLoadImages = document.querySelectorAll('.lazy-load');

  if ('IntersectionObserver' in window) {
      let imageObserver = new IntersectionObserver((entries, observer) => {
          entries.forEach((entry) => {
              if (entry.isIntersecting) {
                  let img = entry.target;
                  img.src = img.getAttribute('data-src');
                  img.onload = () => {
                      img.classList.add('lazy-loaded');
                  };
                  observer.unobserve(img);
              }
          });
      });

      lazyLoadImages.forEach((img) => {
          imageObserver.observe(img);
      });
  } else {
      // Fallback for browsers that don't support Intersection Observer
      let lazyLoadThrottleTimeout;
      function lazyLoad() {
          if (lazyLoadThrottleTimeout) {
              clearTimeout(lazyLoadThrottleTimeout);
          }
          lazyLoadThrottleTimeout = setTimeout(() => {
              let scrollTop = window.pageYOffset;
              lazyLoadImages.forEach((img) => {
                  if (img.offsetTop < window.innerHeight + scrollTop) {
                      img.src = img.getAttribute('data-src');
                      img.onload = () => {
                          img.classList.add('lazy-loaded');
                      };
                  }
              });
              if (lazyLoadImages.length === 0) {
                  document.removeEventListener('scroll', lazyLoad);
                  window.removeEventListener('resize', lazyLoad);
                  window.removeEventListener('orientationChange', lazyLoad);
              }
          }, 20);
      }

      document.addEventListener('scroll', lazyLoad);
      window.addEventListener('resize', lazyLoad);
      window.addEventListener('orientationChange', lazyLoad);
  }
});