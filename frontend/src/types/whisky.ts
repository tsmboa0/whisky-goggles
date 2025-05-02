/**
 * Represents the data structure returned from the whisky bottle detection API
 */
export interface WhiskyData {
  id?: string;
  name: string;
  type?: string;
  region?: string;
  age?: string;
  abv?: string;
  size?: string;
  fair_price: string;
  shelf_price: string;
  avg_msrp?:string;
  confidence_score?:string;
  distillery?: string;
  image_url: string;
  description?: string;
  tasting_notes?: {
    nose?: string;
    palate?: string;
    finish?: string;
  };
  [key: string]: any; // Allow for additional properties
}

// Scan result structure
export interface ScanResult {
  matches: WhiskyData[] | WhiskyData;
}
