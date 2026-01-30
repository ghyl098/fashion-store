import React, { useState } from "react";

const ReviewSection = ({ productId }) => {
  const [reviews, setReviews] = useState([]);
  const [comment, setComment] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!comment.trim()) return;

    const newReview = {
      id: Date.now(),
      text: comment,
    };

    setReviews([...reviews, newReview]);
    setComment("");
  };

  return (
    <div className="review-section">
      <h3>Customer Reviews</h3>

      <form onSubmit={handleSubmit} className="review-form">
        <textarea
          placeholder="Write your review..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />
        <button type="submit">Submit Review</button>
      </form>

      <ul className="review-list">
        {reviews.length === 0 && <p>No reviews yet.</p>}

        {reviews.map((review) => (
          <li key={review.id} className="review-item">
            {review.text}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ReviewSection;
