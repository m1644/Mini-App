const tg = window.Telegram?.WebApp;
if (tg) {
  tg.expand();
  tg.ready();
}

let MENU = { pizza: [], drinks: [] };
let PROMO = {};
let currentTab = 'pizza';
const cart = new Map(); // itemId -> qty

const elList = document.getElementById('list');
const elCart = document.getElementById('cart');
const elCartItems = document.getElementById('cart-items');
const elCartCount = document.getElementById('cart-count');
const elSum = document.getElementById('sum');
const elDiscount = document.getElementById('discount');
const elTotal = document.getElementById('total');

const tabPizza = document.getElementById('tab-pizza');
const tabDrinks = document.getElementById('tab-drinks');
const tabCart = document.getElementById('tab-cart');

const inputAddress = document.getElementById('address');
const inputPhone = document.getElementById('phone');
const selectPayment = document.getElementById('payment');
const inputPromo = document.getElementById('promo');
const btnOrder = document.getElementById('btn-order');

async function loadMenu() {
  const res = await fetch('/api/menu');
  const data = await res.json();
  MENU = data.menu || MENU;
  PROMO = data.promoCodes || {};
  renderList();
}

function renderList() {
  elList.innerHTML = '';
  elCart.classList.add('hidden');
  const items = MENU[currentTab] || [];
  for (const item of items) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <img src="${item.image}" alt="${item.name}" />
      <div class="content">
        <div class="title">${item.name}</div>
        <div class="desc">${item.description}</div>
        <div class="row">
          <div><b>${item.price}₽</b></div>
          <div class="qty" data-id="${item.id}">
            <button class="dec">-</button>
            <span class="q">${cart.get(item.id) || 0}</span>
            <button class="inc">+</button>
          </div>
        </div>
      </div>
    `;
    elList.appendChild(card);
  }
}

function updateCartCount() {
  let count = 0;
  for (const qty of cart.values()) count += qty;
  elCartCount.textContent = String(count);
}

function renderCart() {
  elList.innerHTML = '';
  elCart.classList.remove('hidden');
  elCartItems.innerHTML = '';

  const idToItem = {};
  for (const cat of Object.values(MENU)) for (const it of cat) idToItem[it.id] = it;

  let sum = 0;
  for (const [itemId, qty] of cart.entries()) {
    const item = idToItem[itemId];
    if (!item) continue;
    const line = item.price * qty;
    sum += line;

    const row = document.createElement('div');
    row.className = 'cart-item';
    row.innerHTML = `
      <img src="${item.image}" alt="${item.name}" />
      <div>
        <div class="name">${item.name}</div>
        <div class="muted">${item.price}₽ × ${qty} = <b>${line}₽</b></div>
      </div>
      <div class="qty" data-id="${item.id}">
        <button class="dec">-</button>
        <span class="q">${qty}</span>
        <button class="inc">+</button>
        <button class="remove">×</button>
      </div>
    `;
    elCartItems.appendChild(row);
  }

  const code = (inputPromo.value || '').trim().toUpperCase();
  const pct = PROMO[code] || 0;
  const discount = sum * pct / 100;
  const total = sum - discount;

  elSum.textContent = `${sum.toFixed(2)}₽`;
  elDiscount.textContent = `-${discount.toFixed(2)}₽`;
  elTotal.textContent = `${total.toFixed(2)}₽`;
}

function switchTab(tab) {
  currentTab = tab;
  for (const b of [tabPizza, tabDrinks, tabCart]) b.classList.remove('active');
  if (tab === 'pizza') tabPizza.classList.add('active');
  if (tab === 'drinks') tabDrinks.classList.add('active');
  if (tab === 'cart') tabCart.classList.add('active');

  if (tab === 'cart') renderCart();
  else renderList();
}

document.addEventListener('click', (e) => {
  const t = e.target;
  if (t === tabPizza) return switchTab('pizza');
  if (t === tabDrinks) return switchTab('drinks');
  if (t === tabCart) return switchTab('cart');

  const holder = t.closest('.qty');
  if (holder) {
    const id = Number(holder.dataset.id);
    const qEl = holder.querySelector('.q');
    let q = cart.get(id) || 0;
    if (t.classList.contains('inc')) q++;
    if (t.classList.contains('dec')) q = Math.max(0, q - 1);
    if (t.classList.contains('remove')) q = 0;
    if (q === 0) cart.delete(id); else cart.set(id, q);
    qEl.textContent = String(q);
    updateCartCount();
    if (!elCart.classList.contains('hidden')) renderCart();
  }
});

inputPromo.addEventListener('input', () => {
  if (!elCart.classList.contains('hidden')) renderCart();
});

btnOrder.addEventListener('click', () => {
  const address = (inputAddress.value || '').trim();
  const phone = (inputPhone.value || '').trim();
  const payment = selectPayment.value;
  const promo = (inputPromo.value || '').trim().toUpperCase();

  if (!address || address.length < 5) return alert('Введите корректный адрес');
  if (!phone || phone.replace(/\D/g, '').length < 7) return alert('Введите корректный телефон');
  if (cart.size === 0) return alert('Добавьте товары в корзину');

  const items = [];
  for (const [id, qty] of cart.entries()) items.push({ id, qty });

  const payload = {
    type: 'order',
    items,
    address,
    phone,
    payment,
    promoCode: promo,
  };

  try {
    if (tg?.sendData) {
      tg.sendData(JSON.stringify(payload));
      tg.close();
    } else {
      // Для браузерного теста
      console.log('Order payload', payload);
      alert('Данные заказа отправлены. Откройте Mini App в Telegram, чтобы завершить.');
    }
  } catch (e) {
    console.error(e);
    alert('Ошибка отправки заказа');
  }
});

loadMenu();