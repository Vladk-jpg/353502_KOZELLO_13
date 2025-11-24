function CustomDate(day, month, year) {
  this._day = day;
  this._month = month;
  this._year = year;
}

Object.defineProperty(CustomDate.prototype, 'day', {
  get: function() {
    return this._day;
  },
  set: function(value) {
    if (parseInt(value)) {
      this._day = parseInt(value);
    } else {
      alert("Невалидное значение для дня");
      return;
    }
  }
});

Object.defineProperty(CustomDate.prototype, 'month', {
  get: function() {
    return this._month;
  },
  set: function(value) {
    if (parseInt(value)) {
      this._month = parseInt(value);
    } else {
      alert("Невалидное значение для месяца");
      return;
    }
  }
});

Object.defineProperty(CustomDate.prototype, 'year', {
  get: function() {
    return this._year;
  },
  set: function(value) {
    if (parseInt(value)) {
      this._year = parseInt(value);
    } else {
      alert("Невалидное значение для года");
      return;
    }
  }
});


function DateManager() {
  this._dates = [];
  this._addButton = document.getElementById('add-new-date-button');
  if (this._addButton) {
    var self = this;
    this._addButton.addEventListener('click', function() {
      self.addDate(self.dateInput.value);
    });
  }
  this._dateInput = document.getElementById('add-new-date-input');
  this._showAllDatesButton = document.getElementById('show-all-dates-button');
  if (this._showAllDatesButton) {
    var self = this;
    this._showAllDatesButton.addEventListener('click', function() {
      self.showAllDates();
    });
  }
  this._representDiv = document.getElementById('represent-div-for-dates');
}

DateManager.prototype.showAllDates = function() {
  this.representDiv.innerHTML = '';

  if (this.dates.length === 0) {
    this.representDiv.textContent = 'Нет добавленных дат';
    return;
  }

  var datesList = document.createElement('ul');
  datesList.style.listStyle = 'none';
  datesList.style.padding = '0';

  var self = this;
  this.dates.forEach(function(date, index) {
    var listItem = document.createElement('li');
    var day = String(date.day).padStart(2, '0');
    var month = String(date.month).padStart(2, '0');
    var year = date.year;

    listItem.textContent = 'Дата ' + (index + 1) + ': ' + day + '.' + month + '.' + year;
    datesList.appendChild(listItem);
  });
  this.representDiv.appendChild(datesList);
};

DateManager.prototype.addDate = function(dateString) {
  var dateParts = dateString.split('/');

  if (dateParts.length !== 3) {
    alert("Неверный формат даты. Используйте формат ДД/ММ/ГГГГ");
    return;
  }

  var day = parseInt(dateParts[0], 10);
  var month = parseInt(dateParts[1], 10);
  var year = parseInt(dateParts[2], 10);

  if (isNaN(day) || isNaN(month) || isNaN(year)) {
    alert("Невалидные значения для даты");
    return;
  }
  if (day < 1 || day > 31 || month < 1 || month > 12 || year < 1) {
    alert("Невалидные значения для даты");
    return;
  }

  var customDate = new CustomDate(day, month, year);
  this._dates.push(customDate);
  this.dateInput.value = '';
};

Object.defineProperty(DateManager.prototype, 'dates', {
  get: function() {
    return this._dates;
  },
  set: function(value) {
    if (Array.isArray(value)) {
      var allAreCustomDates = value.every(function(item) {
        return item instanceof CustomDate;
      });
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
});

Object.defineProperty(DateManager.prototype, 'addButton', {
  get: function() {
    return this._addButton;
  },
  set: function(value) {
    if (value instanceof HTMLElement) {
      this._addButton = value;
    } else {
      alert("Невалидное значение для кнопки добавления");
      return;
    }
  }
});

Object.defineProperty(DateManager.prototype, 'dateInput', {
  get: function() {
    return this._dateInput;
  },
  set: function(value) {
    if (value instanceof HTMLElement) {
      this._dateInput = value;
    } else {
      alert("Невалидное значение для поля ввода даты");
      return;
    }
  }
});

Object.defineProperty(DateManager.prototype, 'showAllDatesButton', {
  get: function() {
    return this._showAllDatesButton;
  },
  set: function(value) {
    if (value instanceof HTMLElement) {
      this._showAllDatesButton = value;
    } else {
      alert("Невалидное значение для кнопки показа всех дат");
      return;
    }
  }
});

Object.defineProperty(DateManager.prototype, 'representDiv', {
  get: function() {
    return this._representDiv;
  },
  set: function(value) {
    if (value instanceof HTMLElement) {
      this._representDiv = value;
    } else {
      alert("Невалидное значение для div отображения");
      return;
    }
  }
});

function SpringDateManager() {
  DateManager.call(this);
  
  this._showSpringDatesButton = document.getElementById('show-spring-dates-button');
  this._downloadLink = document.getElementById('download-spring-dates-link');
  if (this._showSpringDatesButton) {
    var self = this;
    this._showSpringDatesButton.addEventListener('click', function() {
      self.showSpringDates();
    });
  }
}

SpringDateManager.prototype = Object.create(DateManager.prototype);
SpringDateManager.prototype.constructor = SpringDateManager;

SpringDateManager.prototype.showSpringDates = function() {
  this.representDiv.innerHTML = '';

  if (this.dates.length === 0) {
    this.representDiv.textContent = 'Нет добавленных дат';
    return;
  }

  var datesList = document.createElement('ul');
  datesList.style.listStyle = 'none';
  datesList.style.padding = '0';

  var self = this;
  var springDates = this.dates.filter(function(value) {
    return value.month === 3 || value.month === 4 || value.month === 5;
  });

  if (springDates.length === 0) {
    this.representDiv.textContent = 'Нет весенних дат';
    return;
  }

  springDates.forEach(function(date, index) {
    var listItem = document.createElement('li');
    var day = String(date.day).padStart(2, '0');
    var month = String(date.month).padStart(2, '0');
    var year = date.year;

    listItem.textContent = 'Дата ' + (index + 1) + ': ' + day + '.' + month + '.' + year;
    datesList.appendChild(listItem);
  });
  this.representDiv.appendChild(datesList);

  var springDatesJson = springDates.map(function(date) {
    return {
      day: date.day,
      month: date.month,
      year: date.year
    };
  });
  var jsonString = JSON.stringify(springDatesJson, null, 2);
  var blob = new Blob([jsonString], { type: 'application/json' });
  var url = URL.createObjectURL(blob);
  if (this._downloadLink) {
    this._downloadLink.href = url;
    this._downloadLink.click();
    URL.revokeObjectURL(url);
  }
};

document.addEventListener('DOMContentLoaded', function() {
  new SpringDateManager();
});

