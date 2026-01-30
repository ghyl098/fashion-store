import React from "react";

const Feedback = () => {
  return (
    <div className="form-container">
      <h2>Feedback</h2>
      <form>
        <input type="text" placeholder="Name" required />
        <input type="email" placeholder="Email" required />
        <textarea placeholder="Your message" required />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Feedback;
