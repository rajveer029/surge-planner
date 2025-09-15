const API_URL = process.env.REACT_APP_API_URL;

export async function getData() {
  const response = await fetch(`${API_URL}/your-endpoint`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
}
