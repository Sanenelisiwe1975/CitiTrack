import { useState, useEffect, useCallback } from 'react';
import { reportsAPI } from '../services/api';

export const useReports = (filters = {}) => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 20,
    total: 0,
    hasMore: false,
  });

  const fetchReports = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await reportsAPI.getAll({
        skip: (pagination.page - 1) * pagination.pageSize,
        limit: pagination.pageSize,
        ...filters,
      });

      setReports(data.reports);
      setPagination({
        page: data.page,
        pageSize: data.page_size,
        total: data.total,
        hasMore: data.has_more,
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [filters, pagination.page, pagination.pageSize]);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  const refresh = () => {
    fetchReports();
  };

  const nextPage = () => {
    if (pagination.hasMore) {
      setPagination(prev => ({ ...prev, page: prev.page + 1 }));
    }
  };

  const prevPage = () => {
    if (pagination.page > 1) {
      setPagination(prev => ({ ...prev, page: prev.page - 1 }));
    }
  };

  return {
    reports,
    loading,
    error,
    pagination,
    refresh,
    nextPage,
    prevPage,
  };
};

export default useReports;