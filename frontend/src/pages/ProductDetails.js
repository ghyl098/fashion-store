import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchProduct } from "../api";

const ProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([
    { user: "Alice", comment: "Great quality!" },
    { user: "Bob", comment: "Loved it!" },
  ]);
  const [newReview, setNewReview] = useState("");

  useEffect(() => {
    fetchProduct(id).then((data) => setProduct(data));
  }, [id]);

  const handleReview = () => {
    if (!newReview) return;
    setReviews([...reviews, { user: "Anonymous", comment: newReview }]);
    setNewReview("");
  };

  if (!product) return <p style={{ padding: "20px" }}>Loading...</p>;

  const imageUrl =
    product.image || `https://source.unsplash.com/400x400/?${product.name}`;

  return (
    <div className="product-details container">
      <div className="details-container">
        <img src={imageUrl} alt={product.name} />
        <div className="info">
          <h2>{product.name}</h2>
          <p>Category: {product.category}</p>
          <p>Price: ${product.price.toFixed(2)}</p>

          <h3>Reviews</h3>
          <ul className="reviews">
            {reviews.map((r, i) => (
              <li key={i}>
                <strong>{r.user}:</strong> {r.comment}
              </li>
            ))}
          </ul>

          <textarea
            placeholder="Write a review..."
            value={newReview}
            onChange={(e) => setNewReview(e.target.value)}
          />
          <button onClick={handleReview}>Submit Review</button>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
