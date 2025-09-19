// Placeholder API utility for Campaigns
const API_BASE_URL = "http://localhost:8000";
const API_KEY = "mysecretapikey"; // Must match the backend API key

export async function createCampaign(data: any) {
  const res = await fetch(`${API_BASE_URL}/campaigns/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': API_KEY,
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create campaign');
  return res.json();
}

export async function getCampaigns() {
  const res = await fetch(`${API_BASE_URL}/campaigns/`, {
    headers: {
      'x-api-key': API_KEY,
    },
  });
  if (!res.ok) throw new Error('Failed to fetch campaigns');
  return res.json();
}

export { API_KEY };
