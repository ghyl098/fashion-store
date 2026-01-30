import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/api";

export const fetchProducts = async () => {
  const res = await axios.get(`${BASE_URL}/products`);
  return res.data;
};

export const fetchCategories = async () => {
  const res = await axios.get(`${BASE_URL}/categories`);
  return res.data;
};

export const fetchProduct = async (id) => {
  const res = await axios.get(`${BASE_URL}/products/${id}`);
  return res.data;
};

export const registerUser = async (data) => {
  const res = await axios.post(`${BASE_URL}/users/register`, data);
  return res.data;
};

export const loginUser = async (data) => {
  const res = await axios.post(`${BASE_URL}/users/login`, data);
  return res.data;
};
