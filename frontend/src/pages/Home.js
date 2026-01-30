import React, { useEffect, useState } from "react";
import { fetchProducts } from "../api";
import ProductCard from "../components/ProductCard";

const Home = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProducts().then((data) => {
      setProducts(data.slice(0, 20)); // show top 20 products
    });
  }, []);

  return (
    <div>
      <div className="hero">
        <h1>Welcome to Fashion Store</h1>
        <p>Discover the latest trends in fashion, accessories & more!</p>
      </div>

      <div className="container">
        <h2 style={{ marginTop: "40px" }}>Top Products</h2>
        <div className="product-grid">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
