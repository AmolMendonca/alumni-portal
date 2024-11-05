import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  }
});

export const searchAlumni = async (query) => {
  try {
    const response = await api.post('/search', {
      query,
      k: 5
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};