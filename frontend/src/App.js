import React, { useEffect, useState } from 'react';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/products/api/')
      .then(response => response.json())
      .then(data => setProducts(data))
      .catch(error => console.error('Errore nella fetch:', error));
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Prodotti disponibili</h1>
      <ul>
        {products.map(product => (
          <li key={product.product_code}>
            <strong>{product.name}</strong> – {product.price.toFixed(2)} €
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
