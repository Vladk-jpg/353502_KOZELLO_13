class CustomDate {
  constructor(day, month, year) {
    this._day = day;
    this._month = month;
    this._year = year;
  }

  get day() {
    return this._day;
  }

  set day(value) {
    if (parseInt(value)) {
      this._day = parseInt(value);
    } else {
      alert("Невалидное значение для дня");
      return;
    }
  }

  get month() {
    return this._month;
  }

  set month(value) {
    if (parseInt(value)) {
      this._month = parseInt(value);
    } else {
      alert("Невалидное значение для месяца");
      return;
    }
  }

  get year() {
    return this._year;
  }

  set year(value) {
    if (parseInt(value)) {
      this._year = parseInt(value);
    } else {
      alert("Невалидное значение для года");
      return;
    }
  }
}

class DateManager {
  constructor() {
    this._dates = [];
    this._addButton = document.getElementById('add-new-date-button');
    this.addButton.addEventListener('click', () => {
      this.addDate(this.dateInput.value);
    });
    this._dateInput = document.getElementById('add-new-date-input');
    this._showAllDatesButton = document.getElementById('show-all-dates-button');
    this.showAllDatesButton.addEventListener('click', () => {
      this.showAllDates();
    });
    this._representDiv = document.getElementById('represent-div-for-dates');
  }

  showAllDates() {
    this.representDiv.innerHTML = '';

    if (this.dates.length === 0) {
      this.representDiv.textContent = 'Нет добавленных дат';
      return;
    }

    const datesList = document.createElement('ul');
    datesList.style.listStyle = 'none';
    datesList.style.padding = '0';

    this.dates.forEach((date, index) => {
      const listItem = document.createElement('li');
      const day = String(date.day).padStart(2, '0');
      const month = String(date.month).padStart(2, '0');
      const year = date.year;

      listItem.textContent = `Дата ${index + 1}: ${day}.${month}.${year}`;
      datesList.appendChild(listItem);
    });
    this.representDiv.appendChild(datesList);
  }

  addDate(dateString) {
    const dateParts = dateString.split('/');

    if (dateParts.length !== 3) {
      alert("Неверный формат даты. Используйте формат ДД/ММ/ГГГГ");
      return;
    }

    const day = parseInt(dateParts[0], 10);
    const month = parseInt(dateParts[1], 10);
    const year = parseInt(dateParts[2], 10);

    if (isNaN(day) || isNaN(month) || isNaN(year)) {
      alert("Невалидные значения для даты");
      return;
    }
    if (day < 1 || day > 31 || month < 1 || month > 12 || year < 1) {
      alert("Невалидные значения для даты");
      return;
    }

    const customDate = new CustomDate(day, month, year);
    this._dates.push(customDate);
    this.dateInput.value = '';
  }

  get dates() {
    return this._dates;
  }

  set dates(value) {
    if (Array.isArray(value)) {
      const allAreCustomDates = value.every(item => item instanceof CustomDate);
      if (allAreCustomDates) {
        this._dates = value;
      } else {
        alert("Все элементы массива должны быть экземплярами CustomDate");
        return;
      }
    } else {
      alert("Невалидное значение для массива дат");
      return;
    }
  }

  get addButton() {
    return this._addButton;
  }

  set addButton(value) {
    if (value instanceof HTMLElement) {
      this._addButton = value;
    } else {
      alert("Невалидное значение для кнопки добавления");
      return;
    }
  }

  get dateInput() {
    return this._dateInput;
  }

  set dateInput(value) {
    if (value instanceof HTMLElement) {
      this._dateInput = value;
    } else {
      alert("Невалидное значение для поля ввода даты");
      return;
    }
  }

  get showAllDatesButton() {
    return this._showAllDatesButton;
  }

  set showAllDatesButton(value) {
    if (value instanceof HTMLElement) {
      this._showAllDatesButton = value;
    } else {
      alert("Невалидное значение для кнопки показа всех дат");
      return;
    }
  }

  get representDiv() {
    return this._representDiv;
  }

  set representDiv(value) {
    if (value instanceof HTMLElement) {
      this._representDiv = value;
    } else {
      alert("Невалидное значение для div отображения");
      return;
    }
  }
}


class SpringDateManager extends DateManager {
  constructor(...args) {
    super(...args);
    this._showSpringDatesButton = document.getElementById('show-spring-dates-button');
    this._downloadLink = document.getElementById('download-spring-dates-link');
    this._showSpringDatesButton.addEventListener('click', () => {
      this.showSpringDates();
    })
  }

  showSpringDates() {
    this.representDiv.innerHTML = '';

    if (this.dates.length === 0) {
      this.representDiv.textContent = 'Нет добавленных дат';
      return;
    }

    const datesList = document.createElement('ul');
    datesList.style.listStyle = 'none';
    datesList.style.padding = '0';

    const springDates = this.dates.filter((value) => {
      return value.month === 3 || value.month === 4 || value.month === 5;
    });

    if (springDates.length === 0) {
      this.representDiv.textContent = 'Нет весенних дат';
      return;
    }

    springDates.forEach((date, index) => {
      const listItem = document.createElement('li');
      const day = String(date.day).padStart(2, '0');
      const month = String(date.month).padStart(2, '0');
      const year = date.year;

      listItem.textContent = `Дата ${index + 1}: ${day}.${month}.${year}`;
      datesList.appendChild(listItem);
    });
    this.representDiv.appendChild(datesList);

    const springDatesJson = springDates.map((date) => {
      return {
        day: date.day,
        month: date.month,
        year: date.year
      };
    });

    const jsonString = JSON.stringify(springDatesJson, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    if (this._downloadLink) {
      this._downloadLink.href = url;
      this._downloadLink.click();
      URL.revokeObjectURL(url);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new SpringDateManager();
})