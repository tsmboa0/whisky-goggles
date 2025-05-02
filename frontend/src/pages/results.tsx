import { useEffect, useState } from "react";
import { useLocation } from "wouter";
import Header from "@/components/header";
import WhiskyDetails from "@/components/whisky-details";
import AdditionalMatches from "@/components/additional-matches";
import { RefreshCcw } from "lucide-react";
import { WhiskyData } from "@/types/whisky";

export default function Results() {
  const [location, setLocation] = useLocation();
  const [bestMatch, setBestMatch] = useState<WhiskyData | null>(null);
  const [additionalMatches, setAdditionalMatches] = useState<WhiskyData[]>([]);

  useEffect(() => {
    // Retrieve the scan results from sessionStorage
    const storedData = sessionStorage.getItem("whiskyData");
    console.log(`the stored data is: ${storedData}`)
    
    if (storedData) {
      const parsedData = JSON.parse(storedData);
      
      // Assuming parsedData.matches is now an array of whisky matches
      if (Array.isArray(parsedData.matches) && parsedData.matches.length > 0) {
        // Set the first match (best match) to display prominently
        setBestMatch(parsedData.matches[0]);
        
        // Set additional matches if there are any
        if (parsedData.matches.length > 1) {
          setAdditionalMatches(parsedData.matches.slice(1));
        }
      } else if (parsedData.matches) {
        // Handle legacy format where matches might be a single object
        setBestMatch(parsedData.matches);
      } else {
        // No matches found, redirect to home page
        setLocation("/");
      }
    } else {
      // If no data is found, redirect to home page
      setLocation("/");
    }
  }, [setLocation]);

  const handleNewScan = () => {
    // Clear the stored data and go back to home page
    sessionStorage.removeItem("whiskyData");
    setLocation("/");
  };

  if (!bestMatch) {
    return (
      <div className="flex items-center justify-center min-h-screen luxury-pattern dark:bg-gray-900">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen luxury-pattern dark:bg-gray-900">
      <div className="max-w-5xl mx-auto p-4 md:p-6">
        <Header />
        
        <main>
          <div className="luxury-card mb-8 dark:bg-gray-800 dark:border-gray-700">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-2xl font-bold text-secondary dark:text-white">Analysis Results</h2>
              <button 
                onClick={handleNewScan}
                className="flex items-center text-primary font-medium hover:underline transition-all"
              >
                <RefreshCcw className="h-5 w-5 mr-2" />
                New Scan
              </button>
            </div>
            
            {/* Best Match Display */}
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-secondary dark:text-white mb-4">Best Match</h3>
              <div className="bottle-container bg-gray-50 dark:bg-gray-700 rounded-lg overflow-hidden">
                <img 
                  src={bestMatch.image_url} 
                  alt={bestMatch.name} 
                  className="max-h-[400px] object-contain mx-auto"
                />
              </div>
            </div>
            
            {/* Best Match Details */}
            <WhiskyDetails whiskyData={bestMatch} />
            
            {/* Additional Matches */}
            {additionalMatches.length > 0 && (
              <div className="mt-12">
                <h3 className="text-xl font-semibold text-secondary dark:text-white mb-6">
                  Additional Matches
                </h3>
                <AdditionalMatches matches={additionalMatches} />
              </div>
            )}
            
            <div className="flex justify-center mt-10">
              <button 
                onClick={handleNewScan} 
                className="gold-button flex items-center py-4 px-8"
              >
                <RefreshCcw className="h-5 w-5 mr-2" />
                Scan Another Bottle
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}