import React, { useState } from 'react';
import { Camera, MapPin, Send, Loader } from 'lucide-react';
import { reportsAPI } from '../services/api';
import { useGeolocation } from '../hooks/useGeolocation';
import { useTranslation } from '../utils/translations';

const ReportForm = ({ language }) => {
  const { t } = useTranslation(language);
  const { location, loading: locationLoading, refreshLocation } = useGeolocation();
  
  const [formData, setFormData] = useState({
    category: 'pothole',
    description: '',
    photo: null,
    photoPreview: null,
    reporter_name: '',
    reporter_phone: '',
    reporter_email: '',
  });
  
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const categories = [
    { value: 'pothole', label: t('categories.pothole') },
    { value: 'streetlight', label: t('categories.streetlight') },
    { value: 'water_leak', label: t('categories.water_leak') },
    { value: 'garbage', label: t('categories.garbage') },
    { value: 'graffiti', label: t('categories.graffiti') },
    { value: 'road_damage', label: t('categories.road_damage') },
    { value: 'traffic_signal', label: t('categories.traffic_signal') },
    { value: 'illegal_dumping', label: t('categories.illegal_dumping') },
    { value: 'other', label: t('categories.other') },
  ];

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData({
        ...formData,
        photo: file,
        photoPreview: URL.createObjectURL(file),
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      // Upload photo if exists
      let photoUrl = null;
      if (formData.photo) {
        const photoResult = await reportsAPI.uploadPhoto(formData.photo);
        photoUrl = photoResult.url;
      }

      // Create report
      const reportData = {
        category: formData.category,
        description: formData.description,
        location: {
          latitude: location?.latitude || -26.2041,
          longitude: location?.longitude || 28.0473,
          address: null,
        },
        photo_url: photoUrl,
        reporter_name: formData.reporter_name || null,
        reporter_phone: formData.reporter_phone || null,
        reporter_email: formData.reporter_email || null,
        language: language,
      };

      const result = await reportsAPI.create(reportData);

      if (result.success) {
        setSuccess(true);
        // Reset form
        setFormData({
          category: 'pothole',
          description: '',
          photo: null,
          photoPreview: null,
          reporter_name: '',
          reporter_phone: '',
          reporter_email: '',
        });
        
        setTimeout(() => setSuccess(false), 5000);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          {t('reportIssue')}
        </h2>

        {success && (
          <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg mb-4">
            Report submitted successfully! {navigator.onLine ? '' : '(Queued for offline submission)'}
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Category */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('category')}
            </label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('description')}
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 h-32 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Describe the issue in detail..."
              required
              minLength={10}
            />
          </div>

          {/* Location */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('location')}
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={location ? `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}` : 'Getting location...'}
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 bg-gray-50"
                readOnly
              />
              <button
                type="button"
                onClick={refreshLocation}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                disabled={locationLoading}
              >
                <MapPin className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Photo */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('photo')} (Optional)
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              {formData.photoPreview ? (
                <div className="space-y-3">
                  <img
                    src={formData.photoPreview}
                    alt="Preview"
                    className="max-h-48 mx-auto rounded-lg"
                  />
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, photo: null, photoPreview: null })}
                    className="text-sm text-red-600 hover:text-red-700"
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <label className="cursor-pointer">
                  <Camera className="w-12 h-12 mx-auto text-gray-400 mb-2" />
                  <p className="text-sm text-gray-600">Click to upload photo</p>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handlePhotoChange}
                    className="hidden"
                  />
                </label>
              )}
            </div>
          </div>

          {/* Contact Info (Optional) */}
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-gray-700">
              Contact Information (Optional)
            </h3>
            
            <input
              type="text"
              placeholder="Your name"
              value={formData.reporter_name}
              onChange={(e) => setFormData({ ...formData, reporter_name: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            
            <input
              type="tel"
              placeholder="Phone number"
              value={formData.reporter_phone}
              onChange={(e) => setFormData({ ...formData, reporter_phone: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            
            <input
              type="email"
              placeholder="Email address"
              value={formData.reporter_email}
              onChange={(e) => setFormData({ ...formData, reporter_email: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={submitting || !location}
            className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {submitting ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Submitting...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>{t('submit')}</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ReportForm;