import React from 'react';
import { MapPin, Calendar, ThumbsUp, Shield } from 'lucide-react';
import { formatDate, formatLocation, getSeverityColor, getStatusColor } from '../utils/formatters';
import { useTranslation } from '../utils/translations';

const ReportCard = ({ report, language }) => {
  const { t } = useTranslation(language);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {/* Photo */}
      {report.photo_url && (
        <img
          src={report.photo_url}
          alt={report.category}
          className="w-full h-48 object-cover"
        />
      )}

      <div className="p-4">
        {/* Header */}
        <div className="flex justify-between items-start mb-3">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {t(`categories.${report.category}`)}
            </h3>
            <p className="text-sm text-gray-500">{report.id}</p>
          </div>
          
          {report.severity && (
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(report.severity)}`}>
              {report.severity.toUpperCase()}
            </span>
          )}
        </div>

        {/* Description */}
        <p className="text-sm text-gray-700 mb-3 line-clamp-2">
          {report.description}
        </p>

        {/* Metadata */}
        <div className="space-y-2 mb-3">
          <div className="flex items-center text-xs text-gray-600">
            <MapPin className="w-4 h-4 mr-1" />
            {formatLocation(report.location)}
          </div>
          
          <div className="flex items-center text-xs text-gray-600">
            <Calendar className="w-4 h-4 mr-1" />
            {formatDate(report.created_at)}
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-between items-center pt-3 border-t border-gray-200">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(report.status)}`}>
            {t(`status.${report.status}`)}
          </span>
          
          <div className="flex items-center space-x-3">
            {report.blockchain_anchors?.length > 0 && (
              <div className="flex items-center text-green-600" title="Blockchain verified">
                <Shield className="w-4 h-4" />
              </div>
            )}
            
            <div className="flex items-center text-gray-600">
              <ThumbsUp className="w-4 h-4 mr-1" />
              <span className="text-xs">{report.upvotes}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportCard;