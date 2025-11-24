const API_BASE_URL = '/properties/api/properties';

class Property {
  constructor(id, title, price, description, category, status, status_display, created_at) {
    this.id = id;
    this.title = title;
    this.price = price;
    this.description = description;
    this.category = category;
    this.status = status;
    this.status_display = status_display;
    this.created_at = created_at;
  }
}

class PropertyManager {
  page = 1;
  limit = 3;
  properties = [];

  constructor() {
    this.init();
  }

  async init() {
    const filterForm = document.querySelector('.catalog-filters form');
    if (filterForm) {
      filterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
          const filters = this.getFiltersFromForm();
          this.properties = await this.fetchProperties(filters);
          this.page = 1;
          this.renderProperties();
        } catch (error) {
          console.error('Error loading properties:', error);
        }
      });
    }

    const limitInput = document.getElementById('pagination-limit');
    if (limitInput) {
      limitInput.addEventListener('change', (e) => {
        const newLimit = parseInt(e.target.value);
        if (newLimit > 0 && newLimit <= 20) {
          this.limit = newLimit;
          this.page = 1;
          this.renderProperties();
        } else {
          e.target.value = this.limit;
        }
      });
      
      limitInput.addEventListener('input', (e) => {
        const value = parseInt(e.target.value);
        if (value < 1) {
          e.target.value = 1;
        } else if (value > 20) {
          e.target.value = 20;
        }
      });
    }

    try {
      const filters = this.getFiltersFromForm();
      this.properties = await this.fetchProperties(filters);
      this.renderProperties();
    } catch (error) {
      console.error('Error loading initial properties:', error);
    }
  }

  renderProperties() {
    const container = document.querySelector('.catalog-properties');
    if (!container) return;

    const grid = container.querySelector('.properties-grid');
    if (!grid) return;

    grid.innerHTML = '';

    const oldPagination = container.querySelector('.properties-pagination');
    if (oldPagination) {
      oldPagination.remove();
    }

    if (!this.properties || this.properties.length === 0) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'catalog-empty';
      emptyDiv.innerHTML = '<p>Нет объектов недвижимости, соответствующих вашим критериям.</p>';
      grid.appendChild(emptyDiv);
      return;
    }

    const totalPages = Math.ceil(this.properties.length / this.limit);
    
    if (this.page > totalPages && totalPages > 0) {
      this.page = totalPages;
    }
    
    if (this.page < 1) {
      this.page = 1;
    }

    const startIndex = (this.page - 1) * this.limit;
    const endIndex = startIndex + this.limit;
    const currentPageProperties = this.properties.slice(startIndex, endIndex);

    currentPageProperties.forEach(property => {
      const card = this.createPropertyCard(property);
      grid.appendChild(card);
    });

    this.initCard3DEffect();

    if (totalPages > 1) {
      this.createPagination(container, totalPages, () => {
        this.renderProperties();
      });
    }
  }

  async fetchProperties(filters = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filters.min_price) {
        params.append('min_price', filters.min_price);
      }
      if (filters.max_price) {
        params.append('max_price', filters.max_price);
      }
      if (filters.category) {
        params.append('category', filters.category);
      }
      if (filters.date_from) {
        params.append('date_from', filters.date_from);
      }
      if (filters.date_to) {
        params.append('date_to', filters.date_to);
      }

      const url = params.toString() 
        ? `${API_BASE_URL}/?${params.toString()}` 
        : `${API_BASE_URL}/`;

      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.properties && Array.isArray(data.properties)) {
        return data.properties.map(p => new Property(
          p.id,
          p.title,
          p.price,
          p.description,
          p.category,
          p.status,
          p.status_display,
          p.created_at
        ));
      }
      
      return [];
    } catch (error) {
      console.error('Error receiving data:', error);
      throw error;
    }
  }

  getFiltersFromForm() {
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');
    const categorySelect = document.getElementById('category');
    const dateFromInput = document.getElementById('date_from');
    const dateToInput = document.getElementById('date_to');

    const filters = {};

    if (minPriceInput && minPriceInput.value) {
      filters.min_price = minPriceInput.value;
    }
    if (maxPriceInput && maxPriceInput.value) {
      filters.max_price = maxPriceInput.value;
    }
    if (categorySelect && categorySelect.value) {
      filters.category = categorySelect.value;
    }
    if (dateFromInput && dateFromInput.value) {
      filters.date_from = dateFromInput.value;
    }
    if (dateToInput && dateToInput.value) {
      filters.date_to = dateToInput.value;
    }

    return filters;
  }

  createPropertyCard(property) {
    const words = property.description.split(' ');
    const truncatedDesc = words.length > 30 
      ? words.slice(0, 30).join(' ') + '...' 
      : property.description;

    const html = `
      <div class="property-card-wrapper" data-property-id="${property.id}">
        <article class="property-card">
          <header>
            <h2>
              ${this.escapeHtml(property.title)}
            </h2>
            <h3>${this.escapeHtml(property.category)}</h3>
          </header>
          
          <section>
            <p>${this.escapeHtml(truncatedDesc)}</p>
          </section>
          
          <section>
            <dl>
              <dt>Цена:</dt>
              <dd class="price-highlight">${property.price} BYN</dd>
              
              <dt>Добавлено:</dt>
              <dd>
                <time datetime="${property.created_at || ''}">
                  ${property.created_at || ''}
                </time>
              </dd>
              
              <dt>Статус:</dt>
              <dd>
                <span class="status-badge status-${property.status.toLowerCase()}">
                  ${this.escapeHtml(property.status_display)}
                </span>
              </dd>
            </dl>
          </section>
        </article>
      </div>
    `;

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html.trim();
    const wrapper = tempDiv.firstElementChild;
    
    wrapper.addEventListener('click', () => {
      window.location.href = `/properties/property/${property.id}/`;
    });
    
    return wrapper;
  }

  initCard3DEffect() {
    const cardWrappers = document.querySelectorAll('.property-card-wrapper');
    
    cardWrappers.forEach(cardWrapper => {
      const card = cardWrapper.querySelector('.property-card');
      
      cardWrapper.addEventListener('mousemove', (event) => {
        const rect = cardWrapper.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const width = rect.width;
        const height = rect.height;
        
        const middleX = width / 2;
        const middleY = height / 2;
        
        const offsetX = ((x - middleX) / middleX) * 15;
        const offsetY = ((y - middleY) / middleY) * 15;
        
        card.style.setProperty('--rotateX', `${offsetX}deg`);
        card.style.setProperty('--rotateY', `${-offsetY}deg`);
      });
      
      cardWrapper.addEventListener('mouseleave', () => {
        card.style.animation = 'reset-card 0.6s ease';
        card.addEventListener('animationend', () => {
          card.style.animation = 'unset';
          card.style.setProperty('--rotateX', '0deg');
          card.style.setProperty('--rotateY', '0deg');
        }, { once: true });
      });
    });
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  createPagination(container, totalPages, renderCallback) {
    const oldPagination = container.querySelector('.properties-pagination');
    if (oldPagination) {
      oldPagination.remove();
    }

    const paginationDiv = document.createElement('div');
    paginationDiv.className = 'properties-pagination';

    const prevButton = document.createElement('button');
    prevButton.className = 'pagination-button';
    prevButton.textContent = '<';
    prevButton.disabled = this.page === 1;
    prevButton.addEventListener('click', () => {
      if (this.page > 1) {
        this.page--;
        renderCallback();
      }
    });
    paginationDiv.appendChild(prevButton);

    const pageNumbers = document.createElement('div');
    pageNumbers.className = 'pagination-numbers';

    let startPage = Math.max(1, this.page - 2);
    let endPage = Math.min(totalPages, startPage + 4);

    if (endPage - startPage < 4) {
      startPage = Math.max(1, endPage - 4);
    }

    for (let i = startPage; i <= endPage; i++) {
      const pageButton = document.createElement('button');
      pageButton.className = 'pagination-button';
      if (i === this.page) {
        pageButton.classList.add('active');
      }
      pageButton.textContent = i;
      pageButton.addEventListener('click', () => {
        this.page = i;
        renderCallback();
      });
      pageNumbers.appendChild(pageButton);
    }

    paginationDiv.appendChild(pageNumbers);

    const nextButton = document.createElement('button');
    nextButton.className = 'pagination-button';
    nextButton.textContent = '>';
    nextButton.disabled = this.page === totalPages;
    nextButton.addEventListener('click', () => {
      if (this.page < totalPages) {
        this.page++;
        renderCallback();
      }
    });
    paginationDiv.appendChild(nextButton);

    container.appendChild(paginationDiv);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new PropertyManager();
});