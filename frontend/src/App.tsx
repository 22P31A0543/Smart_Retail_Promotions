import React, { useState, useEffect } from 'react';
import './App.css';
import { createCampaign, getCampaigns } from './api';

const initialForm = {
  Name: '',
  Description: '',
  StartDate: '',
  EndDate: '',
  DiscountType: '',
  DiscountValue: '',
  Status: '',
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchCampaigns = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getCampaigns();
      setCampaigns(data);
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const payload = {
        ...form,
        DiscountValue: form.DiscountValue ? parseFloat(form.DiscountValue) : 0,
      };
      await createCampaign(payload);
      setSuccess('Campaign created successfully!');
      setForm(initialForm);
      fetchCampaigns();
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Smart Retail Promotions Hub</h1>
      <form className="campaign-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name</label>
          <input name="Name" value={form.Name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea name="Description" value={form.Description} onChange={handleChange} />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Start Date</label>
            <input type="date" name="StartDate" value={form.StartDate} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>End Date</label>
            <input type="date" name="EndDate" value={form.EndDate} onChange={handleChange} required />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Discount Type</label>
            <input name="DiscountType" value={form.DiscountType} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Discount Value</label>
            <input type="number" name="DiscountValue" value={form.DiscountValue} onChange={handleChange} required min="0" step="0.01" />
          </div>
        </div>
        <div className="form-group">
          <label>Status</label>
          <select name="Status" value={form.Status} onChange={handleChange} required>
            <option value="">Select Status</option>
            <option value="Draft">Draft</option>
            <option value="Live">Live</option>
            <option value="Ended">Ended</option>
          </select>
        </div>
        <button type="submit" disabled={loading}>Create Campaign</button>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
      </form>
      <h2>All Campaigns</h2>
      {loading ? <p>Loading...</p> : (
        <div className="campaign-list">
          {campaigns.length === 0 ? <p>No campaigns found.</p> : (
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                  <th>StartDate</th>
                  <th>EndDate</th>
                  <th>DiscountType</th>
                  <th>DiscountValue</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {campaigns.map((c, i) => (
                  <tr key={i}>
                    <td>{c.Name}</td>
                    <td>{c.Description}</td>
                    <td>{c.StartDate}</td>
                    <td>{c.EndDate}</td>
                    <td>{c.DiscountType}</td>
                    <td>{c.DiscountValue}</td>
                    <td>{c.Status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
