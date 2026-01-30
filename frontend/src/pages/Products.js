import React, { useEffect, useState } from "react";
import { fetchProducts, fetchCategories } from "../api";
import ProductCard from "../components/ProductCard";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selected, setSelected] = useState("");

  useEffect(() => {
    fetchProducts().then((data) => setProducts(data));
    fetchCategories().then((data) => setCategories(data));
  }, []);

  const filtered = selected
    ? products.filter((p) => p.category === selected)
    : products;

  return (
    <div className="container">
      <h2 style={{ marginTop: "40px" }}>Our Products</h2>

      <div className="filter">
        <label>Filter by Category:</label>
        <select onChange={(e) => setSelected(e.target.value)} value={selected}>
          <option value="">All</option>
          {categories.map((c) => (
            <option key={c.id} value={c.name}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div className="product-grid">
        {filtered.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
};

export default Products;
