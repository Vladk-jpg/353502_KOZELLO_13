class UrlInput {
  constructor(id, name = '', value = '', placeholder = '', required = false, pattern = '', readonly = false) {
    this.id = id;
    this.name = name;
    this.value = value;
    this.placeholder = placeholder;
    this.required = required;
    this.pattern = pattern;
    this.readonly = readonly;
  }
}

class UrlInputManager {
  constructor() {
    this.inputs = [];
    this.container = document.querySelector('.input-element-container');
    this.addButton = document.querySelector('.input-element-flag');
    this.storageKey = 'urlInputs';
    this.nextId = 1;
    
    this.init();
  }

  init() {
    this.loadFromStorage();
    
    this.renderAll();
    
    if (this.addButton) {
      this.addButton.addEventListener('click', () => {
        this.addInput();
      });
    }
  }

  validateUrl(value, required = false, pattern = '') {
    if (!value || value.trim() === '') {
      if (required) {
        return { valid: false, message: 'Поле не может быть пустым' };
      }
      return { valid: true, message: '' };
    }
    
    if (pattern) {
      try {
        const regex = new RegExp(pattern);
        if (!regex.test(value)) {
          return { valid: false, message: 'Значение не соответствует заданному шаблону' };
        }
      } catch (e) {

      }
    }
    
    try {
      const urlObj = new URL(value);
      if (!['http:', 'https:'].includes(urlObj.protocol)) {
        return { valid: false, message: 'URL должен начинаться с http:// или https://' };
      }
      return { valid: true, message: '' };
    } catch (e) {
      return { valid: false, message: 'Некорректный формат URL' };
    }
  }

  addInput(name = '', value = '', placeholder = '', required = false, pattern = '', readonly = false) {
    const newInput = new UrlInput(this.nextId++, name, value, placeholder, required, pattern, readonly);
    this.inputs.push(newInput);
    this.saveToStorage();
    this.renderAll();
  }

  removeInput(id) {
    this.inputs = this.inputs.filter(input => input.id !== id);
    this.saveToStorage();
    this.renderAll();
  }

  updateInput(id, field, value) {
    const input = this.inputs.find(i => i.id === id);
    if (input) {
      input[field] = value;
      this.saveToStorage();
      if (field === 'value' || field === 'required' || field === 'pattern') {
        this.validateInputElement(id);
      }
      if (field === 'name' || field === 'placeholder' || field === 'pattern' || field === 'readonly' || field === 'required') {
        this.updateInputAttributes(id);
      }
    }
  }

  updateInputAttributes(id) {
    const input = this.inputs.find(i => i.id === id);
    if (!input) return;

    const urlInput = document.querySelector(`#url-input-${id}`);
    if (!urlInput) return;

    if (input.name) {
      urlInput.setAttribute('name', input.name);
    } else {
      urlInput.removeAttribute('name');
    }

    urlInput.placeholder = input.placeholder || 'https://example.com';

    if (input.pattern) {
      urlInput.setAttribute('pattern', input.pattern);
    } else {
      urlInput.removeAttribute('pattern');
    }

    if (input.readonly) {
      urlInput.setAttribute('readonly', 'readonly');
    } else {
      urlInput.removeAttribute('readonly');
    }

    if (input.required) {
      urlInput.setAttribute('required', 'required');
    } else {
      urlInput.removeAttribute('required');
    }
  }

  validateInputElement(id) {
    const input = this.inputs.find(i => i.id === id);
    if (!input) return;

    const urlInput = document.querySelector(`#url-input-${id}`);
    const errorMsg = document.querySelector(`#error-${id}`);
    
    if (!urlInput || !errorMsg) return;

    const validation = this.validateUrl(input.value, input.required, input.pattern);
    
    if (!validation.valid) {
      urlInput.classList.add('invalid');
      errorMsg.textContent = validation.message;
      errorMsg.style.display = 'block';
    } else {
      urlInput.classList.remove('invalid');
      errorMsg.style.display = 'none';
    }
  }

  renderInput(input) {
    const inputDiv = document.createElement('div');
    inputDiv.className = 'url-input-item';
    inputDiv.id = `url-item-${input.id}`;

    inputDiv.innerHTML = `
      <div class="url-input-header">
        <h4>URL Input #${input.id}</h4>
        <button class="delete-btn" data-id="${input.id}">Удалить</button>
      </div>
      <div class="url-input-fields">
        <div class="field-group">
          <label for="url-input-${input.id}">Value (URL):</label>
          <input 
            type="url" 
            id="url-input-${input.id}" 
            class="url-field" 
            value="${this.escapeAttr(input.value)}" 
            name="${this.escapeAttr(input.name)}"
            placeholder="${this.escapeAttr(input.placeholder || 'https://example.com')}"
            pattern="${this.escapeAttr(input.pattern)}"
            ${input.required ? 'required' : ''}
            ${input.readonly ? 'readonly' : ''}
          />
          <span class="error-message" id="error-${input.id}"></span>
        </div>
        <div class="field-group">
          <label for="name-${input.id}">Name:</label>
          <input 
            type="text" 
            id="name-${input.id}" 
            class="settings-field" 
            value="${this.escapeAttr(input.name)}" 
            placeholder="Введите name"
          />
        </div>
        <div class="field-group">
          <label for="placeholder-${input.id}">Placeholder:</label>
          <input 
            type="text" 
            id="placeholder-${input.id}" 
            class="settings-field" 
            value="${this.escapeAttr(input.placeholder)}" 
            placeholder="Введите placeholder"
          />
        </div>
        <div class="field-group">
          <label for="pattern-${input.id}">Pattern:</label>
          <input 
            type="text" 
            id="pattern-${input.id}" 
            class="settings-field" 
            value="${this.escapeAttr(input.pattern)}" 
            placeholder="Введите regex pattern"
          />
        </div>
        <div class="checkbox-group">
          <label>
            <input 
              type="checkbox" 
              id="required-${input.id}" 
              class="settings-checkbox" 
              ${input.required ? 'checked' : ''}
            />
            Required
          </label>
          <label>
            <input 
              type="checkbox" 
              id="readonly-${input.id}" 
              class="settings-checkbox" 
              ${input.readonly ? 'checked' : ''}
            />
            Readonly
          </label>
        </div>
      </div>
    `;

    const urlInput = inputDiv.querySelector(`#url-input-${input.id}`);
    const nameInput = inputDiv.querySelector(`#name-${input.id}`);
    const placeholderInput = inputDiv.querySelector(`#placeholder-${input.id}`);
    const patternInput = inputDiv.querySelector(`#pattern-${input.id}`);
    const requiredCheckbox = inputDiv.querySelector(`#required-${input.id}`);
    const readonlyCheckbox = inputDiv.querySelector(`#readonly-${input.id}`);
    const deleteBtn = inputDiv.querySelector('.delete-btn');

    urlInput.addEventListener('input', (e) => {
      this.updateInput(input.id, 'value', e.target.value);
    });

    urlInput.addEventListener('blur', () => {
      this.validateInputElement(input.id);
    });

    nameInput.addEventListener('input', (e) => {
      this.updateInput(input.id, 'name', e.target.value);
    });

    placeholderInput.addEventListener('input', (e) => {
      this.updateInput(input.id, 'placeholder', e.target.value);
    });

    patternInput.addEventListener('input', (e) => {
      this.updateInput(input.id, 'pattern', e.target.value);
    });

    requiredCheckbox.addEventListener('change', (e) => {
      this.updateInput(input.id, 'required', e.target.checked);
    });

    readonlyCheckbox.addEventListener('change', (e) => {
      this.updateInput(input.id, 'readonly', e.target.checked);
    });

    deleteBtn.addEventListener('click', () => {
      this.removeInput(input.id);
    });

    return inputDiv;
  }

  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  escapeAttr(text) {
    if (!text) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  renderAll() {
    if (!this.container) return;
    
    this.container.innerHTML = '';

    this.inputs.forEach(input => {
      const inputElement = this.renderInput(input);
      this.container.appendChild(inputElement);
      if (input.value) {
        this.validateInputElement(input.id);
      }
    });
  }

  saveToStorage() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.inputs));
    } catch (e) {
      console.error('Ошибка сохранения в localStorage:', e);
    }
  }

  loadFromStorage() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        this.inputs = parsed.map(item => new UrlInput(
          item.id,
          item.name || '',
          item.value || item.url || '',
          item.placeholder || '',
          item.required || false,
          item.pattern || '',
          item.readonly || false
        ));
        if (this.inputs.length > 0) {
          this.nextId = Math.max(...this.inputs.map(i => i.id)) + 1;
        }
      }
    } catch (e) {
      console.error('Ошибка загрузки из localStorage:', e);
      this.inputs = [];
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new UrlInputManager();
});