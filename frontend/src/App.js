import React, { useEffect, useState } from 'react';

function App() {
  const [products, setProducts] = useState([]);
  const [cartItems, setCartItems] = useState([]);
  const [view, setView] = useState("catalog");
  const [checkoutSummary, setCheckoutSummary] = useState(null);

  // Fetch products when component mounts
  useEffect(() => {
    fetch('http://localhost:8000/products/api/')
      .then(response => response.json())
      .then(data => setProducts(data))
      .catch(error => console.error('Errore nella fetch:', error));
  }, []);

  // Add product code to cart
  const addToCart = (code) => {
    setCartItems([...cartItems, code]);
  };

  // Remove the last occurrence of a product code from cart
  const removeFromCart = (code) => {
    const index = cartItems.lastIndexOf(code);
    if (index !== -1) {
      const newCart = [...cartItems];
      newCart.splice(index, 1);
      setCartItems(newCart);
    }
  };

  // Handle checkout button
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
      .catch(err => console.error("Errore nel checkout:", err));
  };

  return (
    <div style={{ padding: '20px' }}>
      {view === "catalog" && (
        <>
          <h1>Prodotti disponibili</h1>
          <ul>
            {products.map(product => (
              <li key={product.product_code}>
                <strong>{product.name}</strong> – {product.price.toFixed(2)} €
                <button onClick={() => addToCart(product.product_code)}>+</button>
                <button onClick={() => removeFromCart(product.product_code)}>-</button>
              </li>
            ))}
          </ul>
          <button onClick={handleCheckout}>
            Vai al Checkout ({cartItems.length} articoli)
          </button>
        </>
      )}

      {view === "checkout" && checkoutSummary && (
        <>
          <h1>Checkout</h1>
          <ul>
            {checkoutSummary.summary.map((item) => (
              <li key={item.product_code}>
                {item.quantity} x {item.name}
              </li>
            ))}
          </ul>
          <p><strong>Totale:</strong> {checkoutSummary.total.toFixed(2)} €</p>
          <button onClick={() => setView("catalog")}>Torna ai prodotti</button>
        </>
      )}
    </div>
  );
}

export default App;
