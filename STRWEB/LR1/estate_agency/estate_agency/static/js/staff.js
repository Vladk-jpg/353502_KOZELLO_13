const API_BASE_URL = '/accounts/api/staff';

function getCsrfToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function getStaffList() {
  try {
    const response = await fetch(API_BASE_URL + '/');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.staff;
  } catch (error) {
    console.error('Error during getting the staff list:', error);
    throw error;
  }
}

function validateStaffData(data) {
  const errors = {};

  if (!data.username || data.username.trim() === '') {
    errors.username = 'Имя пользователя обязательно';
  }

  if (!data.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.email = 'Введите корректный email';
  }

  if (!data.password || data.password.length < 6) {
    errors.password = 'Пароль должен содержать минимум 6 символов';
  }

  const phonePattern8 = /^8\s?(\(0(\d{2})\)|0(\d{2}))\s?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})$/;
  const phonePattern375 = /^\+375\s?(\((\d{2})\)|(\d{2}))\s?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})$/;

  if (!data.phone_number || (!phonePattern8.test(data.phone_number) && !phonePattern375.test(data.phone_number))) {
    errors.phone_number = 'Телефон должен быть в формате: +375 (29) XXX-XX-XX или 8 (029) XXXXXXX';
  }

  if (!data.birth_date || !/^\d{2}\/\d{2}\/\d{4}$/.test(data.birth_date)) {
    errors.birth_date = 'Дата должна быть в формате DD/MM/YYYY';
  } else {
    const [day, month, year] = data.birth_date.split('/').map(Number);
    const birthDate = new Date(year, month - 1, day);
    const today = new Date();
    const age = today.getFullYear() - birthDate.getFullYear() -
      ((today.getMonth() > birthDate.getMonth() ||
        (today.getMonth() === birthDate.getMonth() && today.getDate() >= birthDate.getDate())) ? 0 : 1);

    if (age < 18) {
      errors.birth_date = 'Сотруднику должно быть не менее 18 лет';
    }
  }

  if (!data.position || data.position.trim() === '') {
    errors.position = 'Должность обязательна';
  }

  const experience = parseInt(data.experience);
  if (isNaN(experience) || experience < 0) {
    errors.experience = 'Опыт работы должен быть положительным числом';
  }

  if (!data.url || !/^https?:\/\/.+\.(php|html)$/.test(data.url)) {
    errors.url = 'URL должен начинаться с http:// или https:// и заканчиваться на .php или .html';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

async function addStaff(staffData, photoFile = null) {
  const validation = validateStaffData(staffData);

  if (!validation.isValid) {
    throw new Error(JSON.stringify(validation.errors));
  }

  try {
    const formData = new FormData();

    formData.append('username', staffData.username.trim());
    formData.append('email', staffData.email.trim());
    formData.append('password', staffData.password);
    formData.append('phone_number', staffData.phone_number);
    formData.append('birth_date', staffData.birth_date);
    formData.append('position', staffData.position.trim());
    formData.append('experience', parseInt(staffData.experience));

    if (staffData.first_name) {
      formData.append('first_name', staffData.first_name.trim());
    }
    if (staffData.last_name) {
      formData.append('last_name', staffData.last_name.trim());
    }
    if (staffData.timezone) {
      formData.append('timezone', staffData.timezone);
    }

    if (photoFile) {
      formData.append('photo', photoFile);
    }

    const response = await fetch(API_BASE_URL + '/add/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Ошибка при добавлении сотрудника');
    }

    return data;
  } catch (error) {
    console.error('Ошибка при добавлении сотрудника:', error);
    throw error;
  }
}

class StaffManagement {
  page = 1;
  limit = 3;

  sortBy;
  sortPropertyId;

  staffList = [];
  originalStaffList = [];

  constructor() {
    document.addEventListener('DOMContentLoaded', async () => {
      await this.init();
    });
  }

  async init() {
    try {
      const staffData = await getStaffList();
      this.originalStaffList = staffData.map(staff => ({
        ...staff,
        selected: false
      }));
      this.staffList = [...this.originalStaffList];
    } catch (error) {
      console.error('Не удалось загрузить сотрудников:', error);
    }

    const parent = document.querySelector('.staff-table');
    this.createTable(parent);

    const filterInput = document.getElementById('staff-filter-input');
    const filterButton = document.getElementById('staff-filter-button');

    filterButton.addEventListener('click', () => {
      this.applyFilter();
    });

    filterInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.applyFilter();
      }
    });

    filterInput.addEventListener('input', () => {
      if (filterInput.value.trim() === '') {
        this.resetFilter();
      }
    });

    const addButton = document.querySelector('.staff-add-button');
    if (addButton) {
      addButton.addEventListener('click', () => {
        this.openModal();
      });
    }

    const modalOverlay = document.getElementById('modal-overlay');
    const modalCancel = document.getElementById('modal-cancel');
    const addStaffForm = document.getElementById('add-staff-form');

    modalCancel.addEventListener('click', () => {
      this.closeModal();
    });

    addStaffForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      await this.handleAddStaff();
    });

    this.setupModalValidation();

    const bonusButton = document.getElementById('staff-bonus-button');
    if (bonusButton) {
      bonusButton.addEventListener('click', () => {
        this.handleBonus();
      });
    }
  }

  handleBonus() {
    const selectedStaff = this.originalStaffList.filter(staff => staff.selected === true);
    
    if (selectedStaff.length === 0) {
      const messageElement = document.getElementById('staff-bonus-message');
      messageElement.textContent = 'Не выбрано ни одного сотрудника для премирования';
      return;
    }

    const lastNames = selectedStaff.map(staff => {
      const nameParts = staff.name.trim().split(" ");
      return nameParts.length > 1 ? nameParts[nameParts.length - 1] : staff.name;
    });

    const messageElement = document.getElementById('staff-bonus-message');
    if (lastNames.length === 1) {
      messageElement.textContent = `Сотрудник ${lastNames[0]} будет премирован`;
    } else {
      const namesList = lastNames.join(', ');
      messageElement.textContent = `Сотрудники ${namesList} будут премированы`;
    }
  }

  applyFilter() {
    const filterInput = document.getElementById('staff-filter-input');
    const searchTerm = filterInput.value.trim().toLowerCase();

    if (searchTerm === '') {
      this.resetFilter();
      return;
    }

    this.filterByRow(searchTerm);
  }

  filterByRow(searchTerm) {
    this.staffList = this.originalStaffList.filter((staff) => {
      const name = (staff.name || '').toLowerCase();
      const position = (staff.position || '').toLowerCase();
      const email = (staff.email || '').toLowerCase();
      const phone = (staff.phone || '').toLowerCase();
      const experience = (staff.experience || '').toString();

      return name.includes(searchTerm) ||
             position.includes(searchTerm) ||
             email.includes(searchTerm) ||
             phone.includes(searchTerm) ||
             experience.includes(searchTerm);
    }).map(staff => ({
      ...staff,
      selected: staff.selected || false
    }));

    this.page = 1;
    const parent = document.querySelector('.staff-table');
    this.createTable(parent);
  }

  resetFilter() {
    this.staffList = this.originalStaffList.map(staff => ({
      ...staff,
      selected: staff.selected || false
    }));
    this.page = 1;
    const parent = document.querySelector('.staff-table');
    this.createTable(parent);
  }

  showStaffDetail(staff) {
    const detailSection = document.getElementById('staff-detail');
    
    document.getElementById('staff-detail-name').textContent = staff.name;
    document.getElementById('staff-detail-position').textContent = staff.position;
    document.getElementById('staff-detail-experience').textContent = `${staff.experience} лет`;
    document.getElementById('staff-detail-email').textContent = staff.email;
    document.getElementById('staff-detail-email').href = `mailto:${staff.email}`;
    document.getElementById('staff-detail-phone').textContent = staff.phone;
    document.getElementById('staff-detail-phone').href = `tel:${staff.phone}`;
    
    const photoImg = document.getElementById('staff-detail-photo');
    if (staff.photo_url) {
      photoImg.src = staff.photo_url;
    } else {
      photoImg.src = 'media/staff_photosnoimage.jpg';
    }
    
    detailSection.style.display = 'block';
  }

  openModal() {
    const modalOverlay = document.getElementById('modal-overlay');
    modalOverlay.style.display = 'flex';
    this.checkFormValidity();
  }

  closeModal() {
    const modalOverlay = document.getElementById('modal-overlay');
    modalOverlay.style.display = 'none';
    document.getElementById('add-staff-form').reset();
    this.checkFormValidity();
  }

  setupModalValidation() {
    const allFields = [
      'modal-username',
      'modal-email',
      'modal-password',
      'modal-phone',
      'modal-birth-date',
      'modal-first-name',
      'modal-last-name',
      'modal-position',
      'modal-experience',
      'modal-url',
      'modal-photo'
    ];

    allFields.forEach(fieldId => {
      const field = document.getElementById(fieldId);
      if (field) {
        if (field.type === 'file') {
          field.addEventListener('change', () => {
            this.checkFormValidity();
          });
        } else {
          field.addEventListener('input', () => {
            this.checkFormValidity();
          });
        }
      }
    });
  }

  checkFormValidity() {
    const submitButton = document.getElementById('modal-submit');
    const formData = this.getFormData();
    const validation = validateStaffData(formData);
    
    const allFieldsFilled = 
      formData.username.trim() !== '' &&
      formData.email.trim() !== '' &&
      formData.password.trim() !== '' &&
      formData.phone_number.trim() !== '' &&
      formData.birth_date.trim() !== '' &&
      formData.first_name.trim() !== '' &&
      formData.last_name.trim() !== '' &&
      formData.position.trim() !== '' &&
      formData.experience.trim() !== '' &&
      formData.url.trim() !== '' &&
      document.getElementById('modal-photo').files.length > 0;
    
    submitButton.disabled = !(validation.isValid && allFieldsFilled);
  }

  getFormData() {
    return {
      username: document.getElementById('modal-username').value,
      email: document.getElementById('modal-email').value,
      password: document.getElementById('modal-password').value,
      phone_number: document.getElementById('modal-phone').value,
      birth_date: document.getElementById('modal-birth-date').value,
      first_name: document.getElementById('modal-first-name').value,
      last_name: document.getElementById('modal-last-name').value,
      position: document.getElementById('modal-position').value,
      experience: document.getElementById('modal-experience').value,
      url: document.getElementById('modal-url').value,
      timezone: 'Europe/Moscow'
    };
  }

  async handleAddStaff() {
    const formData = this.getFormData();
    const photoFile = document.getElementById('modal-photo').files[0] || null;
    const preloader = document.getElementById('modal-preloader');
    const form = document.getElementById('add-staff-form');

    const scrollY = window.scrollY;
    document.body.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.top = `-${scrollY}px`;
    document.body.style.width = '100%';

    preloader.style.display = 'flex';
    form.style.opacity = '0.5';
    form.style.pointerEvents = 'none';

    try {
      const result = await addStaff(formData, photoFile);
      console.log('Сотрудник добавлен:', result);
      
      const staffData = await getStaffList();
      this.originalStaffList = staffData.map(staff => ({
        ...staff,
        selected: false
      }));
      this.staffList = [...this.originalStaffList];
      
      const parent = document.querySelector('.staff-table');
      this.createTable(parent);
      
      this.closeModal();
    } catch (error) {
      console.error('Ошибка при добавлении сотрудника:', error);
      try {
        const errors = JSON.parse(error.message);
        alert('Ошибки валидации:\n' + Object.values(errors).join('\n'));
      } catch {
        alert('Ошибка: ' + error.message);
      }
    } finally {
      preloader.style.display = 'none';
      form.style.opacity = '1';
      form.style.pointerEvents = 'auto';
      
      document.body.style.overflow = '';
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      window.scrollTo(0, scrollY);
    }
  }

  sortTableByField(field) {
    let sortField;
    switch (field) {
      case 0: sortField = 'name'; break;
      case 1: sortField = 'position'; break;
      case 2: sortField = 'experience'; break;
      case 3: sortField = 'contacts'; break;
      default: return;
    }

    if (field === this.sortPropertyId) {
      this.sortBy = this.sortBy === 'ASC' ? 'DESC' : 'ASC';
    } else {
      this.sortPropertyId = field;
      this.sortBy = 'ASC';
    }

    this.staffList.sort((a, b) => {
      let valueA, valueB;

      if (sortField === 'experience') {
        valueA = a.experience;
        valueB = b.experience;
        return this.sortBy === 'ASC' ? valueA - valueB : valueB - valueA;
      } else {
        valueA = (a[sortField] || '').toString().toLowerCase();
        valueB = (b[sortField] || '').toString().toLowerCase();

        if (this.sortBy === 'ASC') {
          if (valueA < valueB) return -1;
          if (valueA > valueB) return 1;
          return 0;
        } else {
          if (valueA > valueB) return -1;
          if (valueA < valueB) return 1;
          return 0;
        }
      }
    });

    this.page = 1;
    const parent = document.querySelector('.staff-table');
    this.createTable(parent);
  }

  createTable(container) {
    container.innerHTML = '';

    if (!this.staffList || this.staffList.length === 0) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'staff-empty';
      emptyDiv.innerHTML = '<p>Сотрудники пока не добавлены</p>';
      container.appendChild(emptyDiv);
      return;
    }

    const totalPages = Math.ceil(this.staffList.length / this.limit);
    const startIndex = (this.page - 1) * this.limit;
    const endIndex = startIndex + this.limit;
    const currentPageStaff = this.staffList.slice(startIndex, endIndex);

    const table = document.createElement('table');

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headers = ['Выбрать', 'Фото', 'Имя', 'Должность', 'Опыт работы', 'Контакты'];

    headers.forEach((headerText, index) => {
      const th = document.createElement('th');
      if (index === 0 || index === 1) {
        th.textContent = headerText;
      } else {
        const sortIndex = index - 2;
        if (this.sortPropertyId === sortIndex) {
          if (this.sortBy === 'ASC') {
            th.textContent = headerText + '↑'
          } else {
            th.textContent = headerText + '↓'
          }
        } else {
          th.textContent = headerText + '↑↓';
        }
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
          this.sortTableByField(sortIndex);
        });
      }
      headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');

    currentPageStaff.forEach(staff => {
      const row = document.createElement('tr');

      const checkboxCell = document.createElement('td');
      checkboxCell.className = 'staff-checkbox-cell';
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'staff-checkbox';
      checkbox.checked = staff.selected || false;
      checkbox.addEventListener('change', (e) => {
        e.stopPropagation();
        staff.selected = checkbox.checked;
        const originalStaff = this.originalStaffList.find(s => s.id === staff.id);
        if (originalStaff) {
          originalStaff.selected = checkbox.checked;
        }
      });
      checkboxCell.appendChild(checkbox);
      row.appendChild(checkboxCell);

      const photoCell = document.createElement('td');
      const photoDiv = document.createElement('div');
      photoDiv.className = 'staff-image';
      const img = document.createElement('img');
      if (staff.photo_url) {
        img.src = staff.photo_url;
        img.alt = staff.name;
      } else {
        img.src = 'media/staff_photosnoimage.jpg';
        img.alt = 'Фото сотрудника отсутствует';
      }
      photoDiv.appendChild(img);
      photoCell.appendChild(photoDiv);
      row.appendChild(photoCell);

      const nameCell = document.createElement('td');
      const nameDiv = document.createElement('div');
      nameDiv.className = 'staff-name';
      nameDiv.textContent = staff.name;
      nameCell.appendChild(nameDiv);
      row.appendChild(nameCell);

      const positionCell = document.createElement('td');
      const positionDiv = document.createElement('div');
      positionDiv.className = 'staff-position';
      positionDiv.textContent = staff.position;
      positionCell.appendChild(positionDiv);
      row.appendChild(positionCell);

      const experienceCell = document.createElement('td');
      const experienceDiv = document.createElement('div');
      experienceDiv.className = 'staff-details';
      const experienceDd = document.createElement('dd');
      experienceDd.textContent = `${staff.experience} лет`;
      experienceDiv.appendChild(experienceDd);
      experienceCell.appendChild(experienceDiv);
      row.appendChild(experienceCell);

      const contactsCell = document.createElement('td');
      const contactsDl = document.createElement('dl');
      contactsDl.className = 'staff-details';

      const emailDt = document.createElement('dt');
      emailDt.textContent = 'Email:';
      contactsDl.appendChild(emailDt);

      const emailDd = document.createElement('dd');
      const emailLink = document.createElement('a');
      emailLink.href = `mailto:${staff.email}`;
      emailLink.textContent = staff.email;
      emailDd.appendChild(emailLink);
      contactsDl.appendChild(emailDd);

      const phoneDt = document.createElement('dt');
      phoneDt.textContent = 'Телефон:';
      contactsDl.appendChild(phoneDt);

      const phoneDd = document.createElement('dd');
      const phoneLink = document.createElement('a');
      phoneLink.href = `tel:${staff.phone}`;
      phoneLink.textContent = staff.phone;
      phoneDd.appendChild(phoneLink);
      contactsDl.appendChild(phoneDd);

      contactsCell.appendChild(contactsDl);
      row.appendChild(contactsCell);

      row.addEventListener('click', () => {
        this.showStaffDetail(staff);
        document.querySelectorAll('.staff-table tbody tr').forEach(tr => tr.classList.remove('selected'));
        row.classList.add('selected');
      });

      tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);

    if (totalPages > 1) {
      this.createPagination(container, totalPages);
    }
  }

  createPagination(container, totalPages) {
    const paginationDiv = document.createElement('div');
    paginationDiv.className = 'staff-pagination';

    const prevButton = document.createElement('button');
    prevButton.className = 'pagination-button';
    prevButton.textContent = '<';
    prevButton.disabled = this.page === 1;
    prevButton.addEventListener('click', () => {
      if (this.page > 1) {
        this.page--;
        this.createTable(container);
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
        this.createTable(container);
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
        this.createTable(container);
      }
    });
    paginationDiv.appendChild(nextButton);

    container.appendChild(paginationDiv);
  }

}

new StaffManagement();