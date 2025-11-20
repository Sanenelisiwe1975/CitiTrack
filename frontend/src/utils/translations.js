export const translations = {
  en: {
    appName: 'CitiTrack',
    report: 'Report',
    track: 'Track',
    dashboard: 'Dashboard',
    reportIssue: 'Report an Issue',
    category: 'Category',
    description: 'Description',
    location: 'Location',
    photo: 'Photo',
    submit: 'Submit Report',
    myReports: 'My Reports',
    allReports: 'All Reports',
    status: {
      pending: 'Pending',
      verified: 'Verified',
      in_progress: 'In Progress',
      resolved: 'Resolved',
      rejected: 'Rejected',
    },
    categories: {
      pothole: 'Pothole',
      streetlight: 'Streetlight',
      water_leak: 'Water Leak',
      garbage: 'Garbage',
      graffiti: 'Graffiti',
      road_damage: 'Road Damage',
      traffic_signal: 'Traffic Signal',
      illegal_dumping: 'Illegal Dumping',
      other: 'Other',
    },
    offline: 'You are offline. Reports will be queued.',
    online: 'Back online. Syncing pending reports...',
  },
  zu: {
    appName: 'CitiTrack',
    report: 'Bika',
    track: 'Landelela',
    dashboard: 'Ibhodi',
    reportIssue: 'Bika Inkinga',
    category: 'Isigaba',
    description: 'Incazelo',
    location: 'Indawo',
    photo: 'Isithombe',
    submit: 'Thumela Umbiko',
    myReports: 'Imibiko Yami',
    allReports: 'Yonke Imibiko',
    status: {
      pending: 'Ilindile',
      verified: 'Iqinisekisiwe',
      in_progress: 'Iyaqhubeka',
      resolved: 'Ixazululiwe',
      rejected: 'Yenqatshiwe',
    },
  },
  af: {
    appName: 'CitiTrack',
    report: 'Rapporteer',
    track: 'Volg',
    dashboard: 'Dashboard',
    reportIssue: 'Rapporteer \'n Probleem',
    category: 'Kategorie',
    description: 'Beskrywing',
    location: 'Ligging',
    photo: 'Foto',
    submit: 'Dien Verslag In',
    myReports: 'My Verslae',
    allReports: 'Alle Verslae',
    status: {
      pending: 'Hangende',
      verified: 'Geverifieer',
      in_progress: 'In Proses',
      resolved: 'Opgelos',
      rejected: 'Verwerp',
    },
  },
  st: {
    appName: 'CitiTrack',
    report: 'Tlaleho',
    track: 'Latela',
    dashboard: 'Boto ya Tlhahiso',
    reportIssue: 'Tlaleha Bothata',
    category: 'Sehlopha',
    description: 'Tlhaloso',
    location: 'Sebaka',
    photo: 'Setshwantsho',
    submit: 'Romela Tlaleho',
    myReports: 'Ditlaleho tsa Ka',
    allReports: 'Ditlaleho Tsohle',
    status: {
      pending: 'E Emetse',
      verified: 'E Netefadiitswe',
      in_progress: 'E Tswela Pele',
      resolved: 'E Rarollotswe',
      rejected: 'E Haneduwe',
    },
  },
};

export const useTranslation = (language = 'en') => {
  const t = (key) => {
    const keys = key.split('.');
    let value = translations[language] || translations.en;
    
    for (const k of keys) {
      value = value[k];
      if (!value) break;
    }
    
    return value || key;
  };

  return { t };
};

export default translations;