(function() {
 
  let lastScrollTop = 0;
  let ticking = false;
  
  const houses = document.querySelectorAll('.scroll-house');
  const totalHouses = houses.length;
  
  const startOffset = 200;
  const houseInterval = 300;
  
  function updateHousesVisibility() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    let visibleCount = 0;
    
    if (scrollTop > startOffset) {
      const scrollProgress = scrollTop - startOffset;
      visibleCount = Math.min(
        Math.floor(scrollProgress / houseInterval) + 1,
        totalHouses
      );
    }
    
    houses.forEach((house, index) => {
      if (index < visibleCount) {
        house.classList.add('visible');
      } else {
        house.classList.remove('visible');
      }
    });
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    ticking = false;
  }
  
  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(updateHousesVisibility);
      ticking = true;
    }
  }
  
  window.addEventListener('scroll', onScroll, { passive: true });
  
  window.addEventListener('load', function() {
    updateHousesVisibility();
  });
})();

