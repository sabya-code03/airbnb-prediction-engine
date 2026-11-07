"use client";
import { useState } from "react";

export default function Home() {
  const [formData, setFormData] = useState({
    // Property Basics
    accommodates: 2,
    bedrooms: 1,
    minimum_nights: 1,
    maximum_nights: 365,
    room_type: "Entire home/apt",
    city: "New York",
    // Location
    latitude: 40.730610,
    longitude: -73.935242,
    // Host Details
    host_is_superhost: "t",
    host_has_profile_pic: "t",
    host_identity_verified: "t",
    instant_bookable: "t",
    host_response_time: "within an hour",
    host_total_listings_count: 1,
    host_response_rate: 100,
    host_acceptance_rate: 100,
    // Review Scores
    review_scores_rating: 4.8,
    review_scores_accuracy: 4.8,
    review_scores_cleanliness: 4.8,
    review_scores_checkin: 4.8,
    review_scores_communication: 4.8,
    review_scores_location: 4.8,
    review_scores_value: 4.8,
  });

  const [prediction, setPrediction] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // HTML inputs return strings; cast numerical fields back to numbers for FastAPI
      const payload = {
        ...formData,
        accommodates: Number(formData.accommodates),
        bedrooms: Number(formData.bedrooms),
        minimum_nights: Number(formData.minimum_nights),
        maximum_nights: Number(formData.maximum_nights),
        host_total_listings_count: Number(formData.host_total_listings_count),
        host_response_rate: Number(formData.host_response_rate),
        host_acceptance_rate: Number(formData.host_acceptance_rate),
        latitude: Number(formData.latitude),
        longitude: Number(formData.longitude),
        review_scores_rating: Number(formData.review_scores_rating),
        review_scores_accuracy: Number(formData.review_scores_accuracy),
        review_scores_cleanliness: Number(formData.review_scores_cleanliness),
        review_scores_checkin: Number(formData.review_scores_checkin),
        review_scores_communication: Number(formData.review_scores_communication),
        review_scores_location: Number(formData.review_scores_location),
        review_scores_value: Number(formData.review_scores_value),
      };

      const response = await fetch("https://airbnb-prediction-engine.onrender.com/predictt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(JSON.stringify(errData.detail));
      }

      const data = await response.json();
      setPrediction(data.predicted_price);
    } catch (err: any) {
      setError(err.message || "Failed to fetch prediction");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <main className="min-h-screen bg-gray-950 text-gray-100 flex items-center justify-center p-6">
      <div className="max-w-5xl w-full bg-gray-900 border border-gray-800 rounded-xl shadow-2xl p-8">
        <h1 className="text-3xl font-bold mb-8 text-center text-blue-400">Airbnb Price Predictor Engine</h1>
        
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Property Core */}
          <div>
            <h2 className="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">Property Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Room Type</label>
                <select name="room_type" value={formData.room_type} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none">
                  <option value="Entire home/apt">Entire home/apt</option>
                  <option value="Private room">Private room</option>
                  <option value="Shared room">Shared room</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Accommodates</label>
                <input type="number" name="accommodates" value={formData.accommodates} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Bedrooms</label>
                <input type="number" name="bedrooms" value={formData.bedrooms} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Min Nights</label>
                <input type="number" name="minimum_nights" value={formData.minimum_nights} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none" />
              </div>
            </div>
          </div>

          {/* Host Details */}
          <div>
            <h2 className="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">Host Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Superhost?</label>
                <select name="host_is_superhost" value={formData.host_is_superhost} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none">
                  <option value="t">Yes</option>
                  <option value="f">No</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Response Time</label>
                <select name="host_response_time" value={formData.host_response_time} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none">
                  <option value="within an hour">Within an hour</option>
                  <option value="within a few hours">Within a few hours</option>
                  <option value="within a day">Within a day</option>
                  <option value="a few days or more">A few days or more</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Acceptance Rate (%)</label>
                <input type="number" max="100" name="host_acceptance_rate" value={formData.host_acceptance_rate} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Total Listings</label>
                <input type="number" name="host_total_listings_count" value={formData.host_total_listings_count} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none" />
              </div>
            </div>
          </div>

          {/* Ratings */}
          <div>
            <h2 className="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">Review Scores (0 - 5.0)</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {['rating', 'cleanliness', 'location', 'value'].map((metric) => (
                <div key={metric}>
                  <label className="block text-sm font-medium text-gray-400 mb-1 capitalize">{metric}</label>
                  <input type="number" step="0.1" max="5" name={`review_scores_${metric}`} value={formData[`review_scores_${metric}` as keyof typeof formData]} onChange={handleChange} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:border-blue-500 outline-none" />
                </div>
              ))}
            </div>
          </div>

          <button type="submit" disabled={loading} 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold text-lg py-4 px-4 rounded-lg transition-colors shadow-lg disabled:opacity-50 mt-4">
            {loading ? "Calculating Variance..." : "Predict Optimal Price"}
          </button>
        </form>

        {prediction !== null && (
          <div className="mt-8 p-6 bg-green-950/40 border border-green-800 rounded-xl text-center shadow-inner">
            <p className="text-lg text-green-400 mb-2 font-medium">Model Output: Estimated Nightly Rate</p>
            <p className="text-5xl font-extrabold text-green-300 tracking-tight">${prediction}</p>
          </div>
        )}

        {error && (
          <div className="mt-8 p-6 bg-red-950/40 border border-red-800 rounded-xl text-red-400 overflow-auto max-h-40 font-mono text-sm">
            <span className="font-bold">Execution Error:</span> {error}
          </div>
        )}
      </div>
    </main>
  );
}