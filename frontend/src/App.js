import React, { useEffect, useState } from 'react';
import './App.css';
import { FaShoppingCart } from 'react-icons/fa'; 
import greenTeaImg from './images/green-tea.jpg';
import coffeeImg from './images/coffee.jpg';
import strawberriesImg from './images/strawberry.jpg';
import logo from './images/amenitiz-logo.png';

function App() {
  const [products, setProducts] = useState([]);
  const [cartItems, setCartItems] = useState([]);
  const [view, setView] = useState("catalog");
  const [checkoutSummary, setCheckoutSummary] = useState(null);

  const productImages = {
    GR1: greenTeaImg,
    CF1: coffeeImg,
    SR1: strawberriesImg
  };

  useEffect(() => {
    fetch('http://localhost:8000/products/api/')
      .then(response => response.json())
      .then(data => setProducts(data))
      .catch(error => console.error('Error fetching products:', error));
  }, []);

  const addToCart = (code) => {
    setCartItems([...cartItems, code]);
  };

  const removeFromCart = (code) => {
    const index = cartItems.lastIndexOf(code);
    if (index !== -1) {
      const newCart = [...cartItems];
      newCart.splice(index, 1);
      setCartItems(newCart);
    }
  };

  const handleCheckout = () => {
    fetch("http://localhost:8000/products/checkout/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items: cartItems })
    })
      .then(res => res.json())
      .then(data => {
        setCheckoutSummary(data);
        setView("checkout");
      })
      .catch(err => console.error("Checkout error:", err));
  };

  return (
    <div className="container">
      <header className="navbar">
        <img src={logo} alt="Amenitiz Logo" className="logo" />
      </header>
      {view === "catalog" && (
        <>
          <h2 className="centered-title">Products</h2>

          <div className="product-grid">
            {products.map(product => (
              <div className="product-card" key={product.product_code}>
                <img src={productImages[product.product_code]} alt={product.name} />
                <h3>{product.name}</h3>
                <p>{product.price.toFixed(2)} €</p>
                <div className="buttons">
                  <button onClick={() => addToCart(product.product_code)}>+</button>
                  <button onClick={() => removeFromCart(product.product_code)}>-</button>
                </div>
                <div className="offer">
                  {product.product_code === "GR1" && <p>Buy 1 Get 1 Free</p>}
                  {product.product_code === "SR1" && <p>3+ for 4.50€</p>}
                  {product.product_code === "CF1" && <p>3+ at 2/3 price</p>}
                </div>
              </div>
            ))}
          </div>

          <div className="cart-button-wrapper">
            <button className="checkout-button" onClick={handleCheckout}>
              <FaShoppingCart style={{ marginRight: '8px' }} />
              {cartItems.length}
              <span style={{ marginLeft: '6px' }}>Items</span>
            </button>
          </div>
        </>
      )}

      {view === "checkout" && checkoutSummary && (
        <div className="checkout-wrapper">
          <div className="checkout-items">
            <h2>Checkout</h2>
            <ul>
              {checkoutSummary.summary.map((item) => (
                <li key={item.product_code}>
                  {item.quantity} x {item.name} = {item.subtotal.toFixed(2)} €
                </li>
              ))}
            </ul>
          </div>
          <div className="checkout-summary">
            <h3>Total: {checkoutSummary.total.toFixed(2)} €</h3>
            <button onClick={() => setView("catalog")}>Back to Products</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;