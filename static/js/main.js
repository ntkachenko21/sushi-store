document.addEventListener("DOMContentLoaded", function () {
  // Показ/скрытие скроллбара в меню
  const menu = document.querySelector(".menu-wrapper");
  if (menu) {
    menu.addEventListener("mouseenter", () => {
      menu.classList.add("scroll-visible");
    });

    menu.addEventListener("mouseleave", () => {
      menu.classList.remove("scroll-visible");
    });
  }

  function smoothScrollTo(target) {
  const offset = 30;
  const targetPosition = target.getBoundingClientRect().top + window.scrollY - offset;
  const startPosition = window.scrollY;
  const distance = targetPosition - startPosition;
  const duration = 600;
  let start = null;

  function step(timestamp) {
    if (!start) start = timestamp;
    const progress = timestamp - start;

    const ease = t => t < 0.5
      ? 4 * t * t * t
      : 1 - Math.pow(-2 * t + 2, 3) / 2;

    const percent = Math.min(progress / duration, 1);
    window.scrollTo(0, startPosition + distance * ease(percent));

    if (progress < duration) {
      window.requestAnimationFrame(step);
    }
  }

  window.requestAnimationFrame(step);
}


  // Обработка якорных ссылок
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        e.preventDefault();
        smoothScrollTo(target);
      }
    });
  });

  // Подсветка активной категории при скролле + автопрокрутка
  const sections = document.querySelectorAll('section[id^="category-"]');
  const menuLinks = document.querySelectorAll('.menu-wrapper a');
  const OFFSET = 120;

  function activateMenuLink() {
    const scrollOffset = 30; // отступ для подсветки
    let currentId = null;

    sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top <= scrollOffset && rect.bottom > scrollOffset) {
      currentId = section.id;
    }
  });

    menuLinks.forEach(link => {
      if (link.getAttribute('href') === `#${currentId}`) {
        if (!link.classList.contains("active")) {
          link.classList.add("active");
        }
      } else {
        link.classList.remove("active");
      }
    });
  }

    let scrollTimeout;
  window.addEventListener("scroll", () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      activateMenuLink();
    }, 50);
  });

  activateMenuLink(); // при загрузке
});
