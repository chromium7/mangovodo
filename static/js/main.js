const menuIcon = document.querySelector('.menu');
const menu = document.querySelector('.header');
const overlay = document.querySelector('.overlay');
const close = document.querySelector('.header .subheader .close');

[menuIcon, overlay, close].forEach(widget => widget.addEventListener('click', () => {
    overlay.classList.toggle('active');
    menu.classList.toggle('active');

}));

const left = document.querySelectorAll('.card .left');
const right = document.querySelectorAll('.card .right');
const carousell = document.querySelector('.carousell');

left.forEach( (b) => {
    b.addEventListener('click', () => {
        carousell.style.transform += 'translateX(100vw)';
    })
});

right.forEach( (b) => {
    b.addEventListener('click', () => {
        carousell.style.transform += 'translateX(-100vw)';
    })
});

const profileButton = document.querySelector('.profile-button');
const profileMenu = document.querySelector('.profile-menu');

if (profileButton) {
    profileButton.addEventListener('click', () => {
        profileMenu.classList.toggle('active');
    });
}

const cartButton = document.querySelector('.cart');
const cartOverlay = document.querySelector('.cart-overlay');
const cartContainer = document.querySelector('.cart-container');
const cartClose = document.querySelector('.cart-container .subheader .close');
const cartHeader = document.querySelector('.cart-container .subheader');
const cartProducts = document.querySelector('.cart-products');
const cartTotal = document.querySelector('.cart-container .total span');

[cartButton, cartOverlay, cartClose].forEach(widget => widget.addEventListener('click', (e)=> {
    cartOverlay.classList.toggle('active');
    cartContainer.classList.toggle('active');
}));

if (document.querySelector('.form-add')) {
    const addForms = document.querySelectorAll('.form-add');
    const removeForms = document.querySelectorAll('.form-remove');

    // Adding items to cart
    addForms.forEach(form => {
        form.addEventListener('submit', e => addToCart(e));
    })

    removeForms.forEach(form => {
        form.addEventListener('submit', e => removeFromCart(e))
    })
}

function removeFromCart(e) {
    e.preventDefault();
    let form = e.target;

    let csrf_token = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

    let dataForm = new FormData();

    dataForm.append('csrfmiddlewaretoken', csrf_token);

    fetch(form.action, {
        method: 'POST',
        body: dataForm
    })
    .then(response => response.json())
    .then(result => {
        let totalItems = result.quantity;
        let totalPrice = result.total_price;
        
        cartButton.textContent = `Cart (${totalItems})`;
        cartHeader.textContent = `Your cart -- (${totalItems} items)`;
        cartTotal.textContent = `$ ${totalPrice}`;

        let productContainer = e.target.parentElement.parentElement.parentElement;
        
        cartProducts.removeChild(productContainer);
    });

    return false;
}


function addToCart(e) {
    e.preventDefault();
    let form = e.target;

    let id_quantity = form.querySelector('#id_quantity').value;
    let id_override = form.querySelector('#id_override').value;
    let csrf_token = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

    let dataForm = new FormData();

    dataForm.append('quantity', id_quantity);
    dataForm.append('override', id_override);
    dataForm.append('csrfmiddlewaretoken', csrf_token);

    // Sending a post request using fetch API
    // to update the cart
    fetch(form.action, {
        method: 'POST',
        body: dataForm            
    })
    .then(response => response.json())
    .then(result => {

        let totalItems = result.quantity;
        let totalPrice = result.total_price;

        cartOverlay.classList.add('active');
        cartContainer.classList.add('active');

        cartButton.textContent = `Cart (${totalItems})`;
        cartHeader.textContent = `Your cart -- (${totalItems} items)`;
        cartTotal.textContent = `$ ${totalPrice}`;

        // Loading icon for when fetching the HTML
        cartProducts.innerHTML = `
            <div class='loading'>
                <div class="icon"></div>
            </div>
        `;

        // Fetch the HTML detail for the cart
        fetch('/cart/cart-detail')
        .then(response => response.text())
        .then(html => {
            cartProducts.innerHTML = html;

            let addForms = cartProducts.querySelectorAll('.form-add');
            let removeForms = cartProducts.querySelectorAll('.form-remove');

            addForms.forEach(form => {
                form.addEventListener('submit', e => addToCart(e));
            })
            removeForms.forEach(form => {
                form.addEventListener('submit', e => removeFromCart(e));
            })
        })

        if (!document.querySelector('.checkout-button')) {
            let checkoutButton = document.createElement('div');
            checkoutButton.className = 'checkout-container';
            let checkoutLink = document.createElement('a');
            checkoutLink.className = 'checkout-button';
            checkoutLink.href = '/orders/create/';
            checkoutLink.textContent = 'Checkout';
            checkoutButton.appendChild(checkoutLink);

            cartContainer.appendChild(checkoutButton);
        }
    });

    return false;
}