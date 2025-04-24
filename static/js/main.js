// === Global variable for the product modal ===
let productModalInstance = null;

function openProductModal(productId) {
  fetch(`/products/${productId}/`)
    .then((response) => response.text())
    .then((html) => {
      const modalContent = document.getElementById("productModalContent");
      if (modalContent) {
        modalContent.innerHTML = html;

        const modal = document.getElementById("productModal");
        productModalInstance = new bootstrap.Modal(modal);
        productModalInstance.show();

        const closeButton = modalContent.querySelector(".btn-close-custom");
        if (closeButton) {
          closeButton.addEventListener("click", function () {
            productModalInstance.hide();
          });
        }

        const quantityEl = modalContent.querySelector("#productQuantity");
        const addBtn = modalContent.querySelector("#addToCartBtn");

        let quantity = 1;
        const basePrice = parseFloat(
          addBtn?.dataset.price ||
            addBtn?.textContent.match(/[\d.,]+/)[0].replace(",", "."),
        );

        const updateUI = () => {
          quantityEl.textContent = quantity;
          const totalPrice = (basePrice * quantity)
            .toFixed(2)
            .replace(".", ",");
          addBtn.innerHTML = `Add to cart: ${totalPrice} zł`;
        };

        modalContent
          .querySelector("#increaseQty")
          ?.addEventListener("click", () => {
            quantity++;
            updateUI();
          });

        modalContent
          .querySelector("#decreaseQty")
          ?.addEventListener("click", () => {
            if (quantity > 1) {
              quantity--;
              updateUI();
            }
          });

        updateUI();
      }
    })
    .catch((error) => {
      console.error("Error loading product modal:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("mobileToggle");
  const mobileMenu = document.querySelector(".mobile-menu");
  toggle?.addEventListener("click", () => {
    mobileMenu.classList.toggle("d-none");
  });

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
    const offset = 100;
    const targetPosition =
      target.getBoundingClientRect().top + window.scrollY - offset;
    const startPosition = window.scrollY;
    const distance = targetPosition - startPosition;
    const duration = 600;
    let start = null;

    function step(timestamp) {
      if (!start) start = timestamp;
      const progress = timestamp - start;

      const ease = (t) =>
        t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

      const percent = Math.min(progress / duration, 1);
      window.scrollTo(0, startPosition + distance * ease(percent));

      if (progress < duration) {
        window.requestAnimationFrame(step);
      }
    }

    window.requestAnimationFrame(step);
  }

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        e.preventDefault();
        smoothScrollTo(target);
      }
    });
  });

  const sections = document.querySelectorAll('section[id^="category-"]');
  const menuLinks = document.querySelectorAll(".menu-wrapper a");

  function activateMenuLink() {
    const scrollOffset = 30;
    let currentId = null;

    sections.forEach((section) => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= scrollOffset && rect.bottom > scrollOffset) {
        currentId = section.id;
      }
    });

    menuLinks.forEach((link) => {
      if (link.getAttribute("href") === `#${currentId}`) {
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

  activateMenuLink();

  const closeBtn = document.getElementById("closeCartSidebar");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      const sidebar = document.getElementById("cartSidebar");
      if (sidebar) {
        sidebar.classList.remove("show");
      }
    });
  }

  const openBtn = document.getElementById("openCartSidebar");
  if (openBtn) {
    openBtn.addEventListener("click", () => {
      const sidebar = document.getElementById("cartSidebar");
      if (sidebar) {
        sidebar.classList.add("show");
      }
    });
  }

  const cashOption = document.getElementById("cashOption");
  const paymentOptions = document.querySelectorAll('input[name="payment"]');
  const changeFieldWrapper = document.getElementById("changeFieldWrapper");
  const changeInput = document.getElementById("changeInput");
  const changeAmountSummary = document.getElementById("changeAmountSummary");
  const paymentMethodSummary = document.getElementById("paymentMethodSummary");

  const decreaseBtn = document.getElementById("decreaseQty");
  const increaseBtn = document.getElementById("increaseQty");
  const quantityEl = document.getElementById("productQuantity");
  const personCountSummary = document.getElementById("personCountSummary");

  let quantity = 1;
  let totalPrice = parseFloat(document.body.dataset.totalPrice || "0"); // example: <body data-total-price="112.00">

  // Updating UI for the quantity of people
  function updateQuantityUI() {
    quantityEl.textContent = quantity;
    personCountSummary.textContent = quantity;
  }

  // Toggle visibility of the change field
  function toggleChangeField() {
    if (cashOption.checked) {
      changeFieldWrapper.classList.remove("hidden");
    } else {
      changeFieldWrapper.classList.add("hidden");
      changeAmountSummary.textContent = "—";
    }
  }

  // Update the payment method summary
  function updatePaymentSummary() {
    const selected = document.querySelector('input[name="payment"]:checked');
    const label = selected
      ? document.querySelector(`label[for="${selected.id}"]`)
      : null;
    paymentMethodSummary.textContent = label ? label.textContent.trim() : "";
  }

  // Update the change amount in the summary
  function updateChangeAmountSummary() {
    const value = parseFloat(changeInput.value);
    if (!isNaN(value) && value >= totalPrice) {
      changeAmountSummary.textContent = `${value.toFixed(2)} zł`;
      changeInput.classList.remove("is-invalid");
    } else if (changeInput.value === "") {
      changeAmountSummary.textContent = "—";
      changeInput.classList.remove("is-invalid");
    } else {
      changeAmountSummary.textContent = "—";
      changeInput.classList.add("is-invalid");
    }
  }

  // Validate the change field
  changeInput?.addEventListener("input", () => {
    changeInput.value = changeInput.value.replace(/\D/g, "");
    updateChangeAmountSummary();
  });

  // Event listeners for the number of people
  increaseBtn?.addEventListener("click", () => {
    quantity++;
    updateQuantityUI();
  });

  decreaseBtn?.addEventListener("click", () => {
    if (quantity > 1) {
      quantity--;
      updateQuantityUI();
    }
  });

  // Listeners for changing the payment method
  paymentOptions.forEach((option) => {
    option.addEventListener("change", () => {
      toggleChangeField();
      updatePaymentSummary();
    });
  });

  // Initialization
  updateQuantityUI();
  toggleChangeField();
  updatePaymentSummary();

  const form = document.querySelector("form.checkout-form");
  const submitBtn = document.querySelector(
    'button[type="submit"][form="checkoutForm"]',
  );

  if (submitBtn && form) {
    submitBtn.addEventListener("click", function (e) {
      const requiredFields = form.querySelectorAll("[required]");
      let firstInvalid = null;

      requiredFields.forEach((field) => {
        if (!field.checkValidity()) {
          field.classList.add("is-invalid");

          if (!firstInvalid) {
            firstInvalid = field;
          }
        } else {
          field.classList.remove("is-invalid");
        }
      });

      if (firstInvalid) {
        e.preventDefault();
        const offsetTop =
          firstInvalid.getBoundingClientRect().top + window.scrollY - 120;
        window.scrollTo({ top: offsetTop, behavior: "smooth" });

        // Optional: highlight with a shake or flash animation
        firstInvalid.focus();
      }
    });
  }

  const deliverySelect = document.getElementById("deliverySchedule");
  const pickupSummary = document.getElementById("pickupTimeSummary");

  function generateTimeWindows() {
    const now = new Date();
    now.setMinutes(now.getMinutes() + 30);

    const roundedMinutes = Math.ceil(now.getMinutes() / 10) * 10;
    now.setMinutes(roundedMinutes, 0, 0);

    const options = [];
    for (let i = 0; i < 30; i++) {
      const start = new Date(now.getTime() + i * 10 * 60000);
      const end = new Date(start.getTime() + 10 * 60000);

      const format = (d) => d.toTimeString().slice(0, 5);
      const label = `${format(start)} - ${format(end)}`;

      options.push(label);
    }

    return options;
  }

  function populateSchedule() {
    const windows = generateTimeWindows();
    deliverySelect.innerHTML = "";

    windows.forEach((slot) => {
      const opt = document.createElement("option");
      opt.value = slot;
      opt.textContent = slot;
      deliverySelect.appendChild(opt);
    });

    pickupSummary.textContent = deliverySelect.value;
  }

  deliverySelect?.addEventListener("change", () => {
    pickupSummary.textContent = deliverySelect.value;
  });

  if (deliverySelect) {
    populateSchedule();
  }
});

// === CART: loading and management ===
function toggleCartSidebar(show = true) {
  const sidebar = document.querySelector("#cartSidebar");
  const backdrop = document.querySelector("#cartBackdrop");

  if (!sidebar || !backdrop) return;

  sidebar.classList.toggle("show", show);
  backdrop.classList.toggle("d-none", !show);
  backdrop.classList.toggle("show", show);
  document.body.classList.toggle("cart-open", show);
}

function loadCartSidebar() {
  fetch("/checkout/cart/")
    .then((res) => res.json())
    .then((data) => {
      const container = document.getElementById("cartSidebarContainer");
      if (!container) return;

      container.innerHTML = data.html;
      toggleCartSidebar(true);

      // Close button handling
      const closeBtn = document.getElementById("closeCartSidebar");
      if (closeBtn) {
        closeBtn.addEventListener("click", () => toggleCartSidebar(false));
      }

      // Close by clicking the backdrop
      const backdrop = document.getElementById("cartBackdrop");
      if (backdrop) {
        backdrop.addEventListener("click", () => toggleCartSidebar(false));
      }
    })
    .catch((err) => console.error("Cart load error:", err));
}

// === Adding to cart ===
document.addEventListener("click", function (e) {
  const addBtn = e.target.closest("#addToCartBtn");
  if (!addBtn) return;

  const modal = document.querySelector(".modal-content");
  if (!modal) return;

  const productId = modal.getAttribute("data-product-id");
  const quantityInput = modal.querySelector("#productQuantity");
  const quantity = parseInt(quantityInput.textContent);

  if (!productId || quantity < 1) return;

  fetch("/checkout/add-to-cart/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        updateCartSummary(data.total_quantity, data.total_price);

        if (productModalInstance) {
          productModalInstance.hide();
        }
      } else {
        alert("Something went wrong while adding to cart.");
      }
    })
    .catch((err) => {
      console.error("Add to cart error:", err);
    });
});

// === Update button View Cart ===
function updateCartSummary(quantity, totalPrice) {
  const viewCartBtn = document.querySelector("#viewCartSummary");
  if (viewCartBtn) {
    viewCartBtn.innerHTML = `In the cart: ${quantity} <span>${totalPrice}</span>`;
  }
}

// === Getting CSRF ===
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
