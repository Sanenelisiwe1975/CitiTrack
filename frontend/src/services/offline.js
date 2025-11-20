import Dexie from 'dexie';

// Initialize Dexie database
const db = new Dexie('CitiTrackDB');

db.version(1).stores({
  pendingReports: '++id, timestamp, synced',
  cachedReports: 'id, timestamp',
  settings: 'key',
});

// Offline queue manager
export const offlineQueue = {
  // Add report to queue
  async addReport(reportData) {
    const timestamp = Date.now();
    const id = await db.pendingReports.add({
      ...reportData,
      timestamp,
      synced: false,
    });
    console.log('Report queued for offline submission:', id);
    return id;
  },

  // Get all pending reports
  async getPendingReports() {
    return await db.pendingReports
      .where('synced')
      .equals(false)
      .toArray();
  },

  // Mark report as synced
  async markSynced(id) {
    await db.pendingReports.update(id, { synced: true });
  },

  // Clear synced reports
  async clearSynced() {
    await db.pendingReports
      .where('synced')
      .equals(true)
      .delete();
  },

  // Get pending count
  async getPendingCount() {
    return await db.pendingReports
      .where('synced')
      .equals(false)
      .count();
  },
};

// Cache manager
export const cache = {
  // Save report to cache
  async saveReport(report) {
    await db.cachedReports.put({
      ...report,
      timestamp: Date.now(),
    });
  },

  // Get cached report
  async getReport(id) {
    return await db.cachedReports.get(id);
  },

  // Get all cached reports
  async getAllReports() {
    return await db.cachedReports.toArray();
  },

  // Clear old cache (older than 7 days)
  async clearOldCache() {
    const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    await db.cachedReports
      .where('timestamp')
      .below(sevenDaysAgo)
      .delete();
  },
};

// Settings manager
export const settings = {
  // Save setting
  async set(key, value) {
    await db.settings.put({ key, value });
  },

  // Get setting
  async get(key) {
    const setting = await db.settings.get(key);
    return setting ? setting.value : null;
  },

  // Delete setting
  async delete(key) {
    await db.settings.delete(key);
  },
};

// Sync pending reports when online
export const syncPendingReports = async (api) => {
  if (!navigator.onLine) {
    console.log('Cannot sync: offline');
    return;
  }

  const pending = await offlineQueue.getPendingReports();
  
  if (pending.length === 0) {
    console.log('No pending reports to sync');
    return;
  }

  console.log(`Syncing ${pending.length} pending reports...`);

  for (const report of pending) {
    try {
      // Remove offline-specific fields
      const { id, timestamp, synced, ...reportData } = report;
      
      // Submit report
      const response = await api.post('/api/reports', reportData);
      
      if (response.status === 201) {
        await offlineQueue.markSynced(report.id);
        console.log('Report synced:', report.id);
      }
    } catch (error) {
      console.error('Failed to sync report:', error);
    }
  }

  // Clear synced reports
  await offlineQueue.clearSynced();
  
  console.log('Sync completed');
};

export default db;