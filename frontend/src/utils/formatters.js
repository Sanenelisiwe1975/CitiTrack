/**
 * Utility functions for formatting data
 */

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;
  
  // Less than a minute
  if (diff < 60000) {
    return 'Just now';
  }
  
  // Less than an hour
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000);
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  }
  
  // Less than a day
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  }
  
  // Less than a week
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000);
    return `${days} day${days > 1 ? 's' : ''} ago`;
  }
  
  // Format as date
  return date.toLocaleDateString('en-ZA', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatLocation = (location) => {
  if (location.address) {
    return location.address;
  }
  return `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}`;
};

export const formatPhoneNumber = (phone) => {
  // Format South African phone numbers
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.startsWith('27')) {
    return `+${cleaned.slice(0, 2)} ${cleaned.slice(2, 4)} ${cleaned.slice(4, 7)} ${cleaned.slice(7)}`;
  }
  
  if (cleaned.startsWith('0')) {
    return `${cleaned.slice(0, 3)} ${cleaned.slice(3, 6)} ${cleaned.slice(6)}`;
  }
  
  return phone;
};

export const formatReportId = (id) => {
  return id.toUpperCase();
};

export const getSeverityColor = (severity) => {
  const colors = {
    low: 'text-green-600 bg-green-100',
    medium: 'text-yellow-600 bg-yellow-100',
    high: 'text-orange-600 bg-orange-100',
    critical: 'text-red-600 bg-red-100',
  };
  return colors[severity] || colors.low;
};

export const getStatusColor = (status) => {
  const colors = {
    pending: 'text-gray-600 bg-gray-100',
    verified: 'text-blue-600 bg-blue-100',
    in_progress: 'text-yellow-600 bg-yellow-100',
    resolved: 'text-green-600 bg-green-100',
    rejected: 'text-red-600 bg-red-100',
  };
  return colors[status] || colors.pending;
};

export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};