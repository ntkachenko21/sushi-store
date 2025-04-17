function openProductModal(productId) {
  fetch(`/product/${productId}/`)
    .then(response => response.text())
    .then(html => {
      const modalContent = document.getElementById("productModalContent");
      if (modalContent) {
        modalContent.innerHTML = html;

        const modal = document.getElementById("productModal");
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();

        const closeButton = modalContent.querySelector(".btn-close-custom");
        if (closeButton) {
          closeButton.addEventListener("click", function () {
            modalInstance.hide();
          });
        }
      }
    })
    .catch(error => {
      console.error("Error loading product modal:", error);
    });
}

// Всё остальное — внутри DOMContentLoaded
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

  // Плавная прокрутка якоря
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

  // Подсветка активной категории при скролле + debounce
  const sections = document.querySelectorAll('section[id^="category-"]');
  const menuLinks = document.querySelectorAll('.menu-wrapper a');

  function activateMenuLink() {
    const scrollOffset = 30;
    let currentId = null;

    sections.forEach(section => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= scrollOffset && rect.bottom > scrollOffset) {
        currentId = section.id;
      }
    });

    menuLinks.forEach(link => {
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add("active");
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


// === КОРЗИНА: загрузка и управление ===

function toggleCartSidebar(show = true) {
  const sidebar = document.querySelector('#cartSidebar');
  if (sidebar) {
    sidebar.classList.toggle('show', show);
  }
}

function loadCartSidebar() {
  fetch('/checkout/cart/')
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('cartSidebarContainer');
      if (container) {
        container.innerHTML = data.html;

        // Показать
        toggleCartSidebar(true);

        // Назначить обработчик кнопки закрытия
        const closeBtn = document.getElementById('closeCartSidebar');
        if (closeBtn) {
          closeBtn.addEventListener('click', () => toggleCartSidebar(false));
        }
      }
    })
    .catch(err => console.error('Cart load error:', err));
}

// === Обработка кнопок + и - и обновление суммы ===

document.addEventListener("click", function (e) {
  const quantityEl = document.getElementById("productQuantity");
  const addBtn = document.getElementById("addToCartBtn");

  if (!quantityEl || !addBtn) return;

  let quantity = parseInt(quantityEl.textContent) || 1;
  const priceText = addBtn.textContent.match(/(\d+[.,]?\d*)/);
  const basePrice = priceText ? parseFloat(priceText[1].replace(",", ".")) / quantity : 0;

  if (e.target.closest("#increaseQty")) quantity++;
  if (e.target.closest("#decreaseQty") && quantity > 1) quantity--;

  quantityEl.textContent = quantity;
  const totalPrice = (basePrice * quantity).toFixed(2).replace(".", ",");
  addBtn.innerHTML = `Add to cart: ${totalPrice} zł`;
});