class Slider {
  images = [
    '/media/slider/banner_1.png',
    '/media/slider/banner_2.png',
    '/media/slider/banner_3.png'
  ];

  titles = [
    'Баннер 1',
    'Баннер 2',
    'Баннер 3'
  ];

  currentIndex = 0;
  autoInterval = null;

  loop = true;
  navs = true;
  pags = true;
  auto = true;
  stopMouseHover = true;
  delay = 2000;

  constructor() {
    document.addEventListener('DOMContentLoaded', () => {
      this.init();
    });
  }

  init() {
    const prevButton = document.querySelector('.slider-left-button');
    const nextButton = document.querySelector('.slider-right-button');
    const sliderImg = document.querySelector('.slider-img');
    const sliderTitle = document.querySelector('.slider-title');
    const pagination = document.querySelector('.slider-pagination');

    if (pagination && this.pags) {
      this.createPagination(pagination);
    }

    prevButton.addEventListener('click', () => {
      this.prevSlide();
    });

    nextButton.addEventListener('click', () => {
      this.nextSlide();
    });

    this.updateSlide(sliderImg, sliderTitle);

    if (this.auto) {
      this.startAutoSlide();
    }

    const sliderWrapper = document.querySelector('.slider-image-wrapper');
    if (sliderWrapper) {
      sliderWrapper.addEventListener('mouseenter', () => {
        if (this.stopMouseHover && this.auto) {
          this.stopAutoSlide();
        }
      });
      sliderWrapper.addEventListener('mouseleave', () => {
        if (this.stopMouseHover && this.auto) {
          this.startAutoSlide();
        }
      });
    }

    this.initSettings();
  }

  initSettings() {
    const loopCheckbox = document.getElementById('slider-loop');
    const navsCheckbox = document.getElementById('slider-navs');
    const pagsCheckbox = document.getElementById('slider-pags');
    const autoCheckbox = document.getElementById('slider-auto');
    const stopMouseHoverCheckbox = document.getElementById('slider-stopMouseHover');
    const delayInput = document.getElementById('slider-delay');

    if (loopCheckbox) {
      loopCheckbox.checked = this.loop;
      loopCheckbox.addEventListener('change', (e) => {
        this.setLoop(e.target.checked);
      });
    }

    if (navsCheckbox) {
      navsCheckbox.checked = this.navs;
      navsCheckbox.addEventListener('change', (e) => {
        this.setNavs(e.target.checked);
      });
    }

    if (pagsCheckbox) {
      pagsCheckbox.checked = this.pags;
      pagsCheckbox.addEventListener('change', (e) => {
        this.setPags(e.target.checked);
      });
    }

    if (autoCheckbox) {
      autoCheckbox.checked = this.auto;
      autoCheckbox.addEventListener('change', (e) => {
        this.setAuto(e.target.checked);
        this.updateAutoSettings();
      });
    }

    if (stopMouseHoverCheckbox) {
      stopMouseHoverCheckbox.checked = this.stopMouseHover;
      stopMouseHoverCheckbox.addEventListener('change', (e) => {
        this.setStopMouseHover(e.target.checked);
      });
    }

    if (delayInput) {
      delayInput.value = this.delay;
      delayInput.addEventListener('blur', (e) => {
        const value = parseInt(e.target.value);
        if (!isNaN(value) && value >= 100) {
          this.setDelay(value);
        } else {
          e.target.value = this.delay;
          alert('Задержка должна быть не менее 100 мс');
        }
      });
    }

    this.updateAutoSettings();
  }

  updateAutoSettings() {
    const stopMouseHoverCheckbox = document.getElementById('slider-stopMouseHover');
    const delayInput = document.getElementById('slider-delay');

    if (stopMouseHoverCheckbox) {
      stopMouseHoverCheckbox.disabled = !this.auto;
    }

    if (delayInput) {
      delayInput.disabled = !this.auto;
    }
  }

  setLoop(value) {
    this.loop = value;
  }

  setNavs(value) {
    this.navs = value;
    const sliderNumber = document.querySelector('.slider-number');
    if (sliderNumber) {
      if (this.navs) {
        sliderNumber.textContent = `${this.currentIndex + 1} / ${this.titles.length}`;
      } else {
        sliderNumber.textContent = '';
      }
    }
  }

  setPags(value) {
    this.pags = value;
    const pagination = document.querySelector('.slider-pagination');
    if (pagination) {
      if (this.pags) {
        this.createPagination(pagination);
      } else {
        pagination.innerHTML = '';
      }
    }
  }

  setAuto(value) {
    this.auto = value;
    if (this.auto) {
      this.startAutoSlide();
    } else {
      this.stopAutoSlide();
    }
  }

  setStopMouseHover(value) {
    this.stopMouseHover = value;
    if (this.auto) {
      this.startAutoSlide();
    }
  }

  setDelay(value) {
    this.delay = value;
    if (this.auto) {
      this.startAutoSlide();
    }
  }

  createPagination(container) {
    container.innerHTML = '';
    
    for (let i = 0; i < this.images.length; i++) {
      const dot = document.createElement('div');
      dot.className = 'slider-pagination-dot';
      if (i === this.currentIndex) {
        dot.classList.add('active');
      }
      
      dot.addEventListener('click', () => {
        this.goToSlide(i);
      });
      
      container.appendChild(dot);
    }
  }

  goToSlide(index) {
    if (index >= 0 && index < this.images.length) {
      this.currentIndex = index;
      this.updateSlide();
    }
  }

  prevSlide() {
    if (this.loop) {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
    } else {
      this.currentIndex = this.currentIndex > 0 ? this.currentIndex - 1 : this.currentIndex;
    }
    this.updateSlide();
  }

  nextSlide() {
    if (this.loop) {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
    } else {
      this.currentIndex = this.currentIndex < this.images.length - 1 ? this.currentIndex + 1 : this.currentIndex;
    }
    this.updateSlide();
  }

  startAutoSlide() {
    this.stopAutoSlide();
    
    const delayMs = this.delay || 5000;
    
    this.autoInterval = setInterval(() => {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
      this.updateSlide();
    }, delayMs);
  }

  stopAutoSlide() {
    if (this.autoInterval) {
      clearInterval(this.autoInterval);
      this.autoInterval = null;
    }
  }

  updateSlide() {
    const sliderImg = document.querySelector('.slider-img');
    const sliderTitle = document.querySelector('.slider-title');
    const sliderNumber = document.querySelector('.slider-number');
    const paginationDots = document.querySelectorAll('.slider-pagination-dot');

    if (sliderImg) {
      sliderImg.src = this.images[this.currentIndex];
    }
    if (sliderTitle) {
      sliderTitle.textContent = this.titles[this.currentIndex];
    }
    if (sliderNumber) {
      if (this.navs) {
        sliderNumber.textContent = `${this.currentIndex + 1} / ${this.titles.length}`;
      } else {
        sliderNumber.textContent = '';
      }
    }
    
    if (paginationDots) {
      paginationDots.forEach((dot, index) => {
        if (index === this.currentIndex) {
          dot.classList.add('active');
        } else {
          dot.classList.remove('active');
        }
      });
    }
  }
}

const slider = new Slider();