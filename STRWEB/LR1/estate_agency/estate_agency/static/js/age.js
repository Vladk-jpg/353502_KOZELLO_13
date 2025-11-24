(function () {
  const hasShownPrompt = localStorage.getItem('agePromptShown');

  if (!hasShownPrompt) {
    const birthDateInput = prompt('Пожалуйста, введите вашу дату рождения (формат: ДД/ММ/ГГГГ):');

    if (birthDateInput) {
      const dateParts = birthDateInput.split('/');

      if (dateParts.length === 3) {
        const day = parseInt(dateParts[0], 10);
        const month = parseInt(dateParts[1], 10) - 1;
        const year = parseInt(dateParts[2], 10);

        const birthDate = new Date(year, month, day);
        const today = new Date();

        if (birthDate.getDate() === day &&
          birthDate.getMonth() === month &&
          birthDate.getFullYear() === year &&
          birthDate <= today) {

          let age = today.getFullYear() - birthDate.getFullYear();
          const monthDiff = today.getMonth() - birthDate.getMonth();

          if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
          }

          if (age < 18) {
            alert('Для использования сайта необходимо разрешение родителей.');
          } else {
            const daysOfWeek = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
            const dayOfWeek = daysOfWeek[birthDate.getDay()];
            alert(`День недели вашего рождения: ${dayOfWeek}`);
          }
          localStorage.setItem('agePromptShown', 'true');
        } else {
          alert('Введена некорректная дата. Пожалуйста, обновите страницу и попробуйте снова.');
        }
      } else {
        alert('Неверный формат даты. Используйте формат ДД.ММ.ГГГГ');
      }
    }
  }
})();

