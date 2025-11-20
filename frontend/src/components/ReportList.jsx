import React, { useState } from 'react';
import { Search, Filter } from 'lucide-react';
import { useReports } from '../hooks/useReports';
import ReportCard from './ReportCard';
import { useTranslation } from '../utils/translations';

const ReportList = ({ language }) => {
  const { t } = useTranslation(language);
  const [filters, setFilters] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  
  const { reports, loading, pagination, nextPage, prevPage } = useReports(filters);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">{t('allReports')}</h2>
        
        {/* Search and Filter */}
        <div className="flex space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search reports..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center space-x-2">
            <Filter className="w-5 h-5" />
            <span>Filter</span>
          </button>
        </div>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports.map(report => (
          <ReportCard key={report.id} report={report} language={language} />
        ))}
      </div>

      {/* Pagination */}
      {reports.length > 0 && (
        <div className="mt-8 flex justify-between items-center">
          <button
            onClick={prevPage}
            disabled={pagination.page === 1}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          <span className="text-sm text-gray-600">
            Page {pagination.page} of {Math.ceil(pagination.total / pagination.pageSize)}
          </span>
          
          <button
            onClick={nextPage}
            disabled={!pagination.hasMore}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}

      {reports.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No reports found</p>
        </div>
      )}
    </div>
  );
};

export default ReportList;