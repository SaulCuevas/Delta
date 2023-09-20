    
    window.sr = ScrollReveal();
    
    sr.reveal('.navbar', {
      duration: 1500,
      origin: 'bottom',
      reset: true
    });
    
    sr.reveal('#header', {
      duration: 1500,
      origin: 'left',
      distance: '200px',
      delay: 500,
      reset: true
    });

    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
        });
      });
    });
    



  
  