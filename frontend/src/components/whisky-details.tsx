import React from "react";
import { WhiskyData } from "@/types/whisky";

interface WhiskyDetailsProps {
  whiskyData: WhiskyData;
}

export default function WhiskyDetails({ whiskyData }: WhiskyDetailsProps) {
  // Extract tasting notes if they exist in a structured format
  const tastingNotes = whiskyData.tasting_notes || {
    nose: "",
    palate: "",
    finish: "",
  };

  return (
    <div className="whisky-details">
      {/* Primary Info */}
      <div className="mb-6 text-center">
        <h1 className="text-3xl font-bold mb-2 gradient-text">{whiskyData.name}</h1>
        <p className="text-gray-600 dark:text-gray-300 text-lg">{whiskyData.type || "Whisky"}</p>
      </div>
      
      {/* Details Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Product Details Section */}
        <div className="luxury-card bg-gray-50 dark:bg-gray-700 p-6 border-0">
          <div className="flex items-center mb-4">
            <div className="w-10 h-10 rounded-full bg-primary/10 dark:bg-primary/20 flex items-center justify-center mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-secondary dark:text-white">Product Details</h3>
          </div>
          
          <div className="space-y-0.5">
            <DetailItem label="Confidence Score" value={
              typeof whiskyData.confidence_score === 'number'
                ? `${(whiskyData.confidence_score * 100).toFixed(0)}%`
                : whiskyData.confidence_score
            } />
            <DetailItem label="Age" value={whiskyData.age} />
            <DetailItem label="ABV" value={whiskyData.abv ? `${whiskyData.abv}%` : undefined} />
            {whiskyData.fair_price && (
              <DetailItem label="Fair Price" value={whiskyData.fair_price} />
            )}
            {whiskyData.shelf_price && (
              <DetailItem label="Shelf Price" value={whiskyData.shelf_price} />
            )}
            {whiskyData.avg_msrp && (
              <DetailItem label="Avg. MSRP" value={whiskyData.avg_msrp} />
            )}
          </div>
        </div>

        {/* Tasting notes */}
        <div className="luxury-card bg-gray-50 dark:bg-gray-700 p-6 border-0">
          <div className="flex items-center mb-4">
            <div className="w-10 h-10 rounded-full bg-primary/10 dark:bg-primary/20 flex items-center justify-center mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-secondary dark:text-white">Tasting Notes</h3>
          </div>
          
          <div className="space-y-4">
            {tastingNotes.nose && (
              <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
                <p className="text-gray-800 dark:text-gray-200">
                  <span className="text-primary font-semibold block mb-1">Nose:</span>
                  {tastingNotes.nose}
                </p>
              </div>
            )}
            
            {tastingNotes.palate && (
              <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
                <p className="text-gray-800 dark:text-gray-200">
                  <span className="text-primary font-semibold block mb-1">Palate:</span>
                  {tastingNotes.palate}
                </p>
              </div>
            )}
            
            {tastingNotes.finish && (
              <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
                <p className="text-gray-800 dark:text-gray-200">
                  <span className="text-primary font-semibold block mb-1">Finish:</span>
                  {tastingNotes.finish}
                </p>
              </div>
            )}
            
            {!tastingNotes.nose && !tastingNotes.palate && !tastingNotes.finish && (
              <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
                <p className="text-gray-600 dark:text-gray-400 italic">No tasting notes available</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

interface DetailItemProps {
  label: string;
  value: string | number | undefined;
}

function DetailItem({ label, value }: DetailItemProps) {
  if (!value) return null;
  
  return (
    <div className="flex justify-between py-3 px-2 border-b border-gray-200/70 dark:border-gray-600/50 last:border-0 hover:bg-white dark:hover:bg-gray-800 rounded transition-colors">
      <span className="text-gray-600 dark:text-gray-400 font-medium">{label}</span>
      <span className="font-semibold text-gray-800 dark:text-white">{value}</span>
    </div>
  );
}