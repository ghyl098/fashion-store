import React from "react";
import { Link } from "react-router-dom";

const ProductCard = ({ product }) => {
  // If backend has empty image, use Unsplash placeholder
  const imageUrl =
    product.image || `https://source.unsplash.com/400x400/?${product.name}`;

  return (
    <div className="product-card">
      <img src={imageUrl} alt={product.name} />
      <h3>{product.name}</h3>
      <p>${product.price.toFixed(2)}</p>
      <Link to={`/products/${product.id}`} className="view-btn">
        View Details
      </Link>
    </div>
  );
};

export default ProductCard;
