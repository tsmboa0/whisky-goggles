import { useState } from "react";
import { WhiskyData } from "@/types/whisky";
import WhiskyDetails from "@/components/whisky-details";
import { ChevronDown, ChevronUp } from "lucide-react";

interface AdditionalMatchesProps {
  matches: WhiskyData[];
}

export default function AdditionalMatches({ matches }: AdditionalMatchesProps) {
  const [expandedMatch, setExpandedMatch] = useState<number | null>(null);

  const toggleExpand = (index: number) => {
    setExpandedMatch(expandedMatch === index ? null : index);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6">
      {matches.map((match, index) => (
        <div 
          key={`${match.name}-${index}`}
          className="luxury-card bg-gray-50 dark:bg-gray-700 p-4 overflow-hidden transition-all duration-300 hover:shadow-lg"
        >
          <div className="flex items-start space-x-4">
            {/* Thumbnail */}
            <div className="w-20 h-20 md:w-24 md:h-24 flex-shrink-0 bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
              <img 
                src={match.image_url} 
                alt={match.name} 
                className="w-full h-full object-contain"
              />
            </div>
            
            {/* Basic Details */}
            <div className="flex-1 min-w-0">
              <h4 className="text-lg font-semibold text-secondary dark:text-white truncate">
                {match.name}
              </h4>
              <div className="mt-1 flex flex-wrap gap-x-4 gap-y-1 text-sm">
                {match.type && (
                  <span className="text-gray-600 dark:text-gray-300">{match.type}</span>
                )}
                {match.confidence_score && (
                  <span className="text-gray-600 dark:text-gray-300">
                    Match: {typeof match.confidence_score === 'number' 
                      ? `${(match.confidence_score * 100).toFixed(0)}%` 
                      : match.confidence_score}
                  </span>
                )}
              </div>
              
              {/* Toggle button */}
              <button 
                onClick={() => toggleExpand(index)}
                className="mt-2 flex items-center text-primary text-sm font-medium hover:underline"
              >
                {expandedMatch === index ? (
                  <>
                    <span>Show less</span>
                    <ChevronUp className="ml-1 h-4 w-4" />
                  </>
                ) : (
                  <>
                    <span>Show details</span>
                    <ChevronDown className="ml-1 h-4 w-4" />
                  </>
                )}
              </button>
            </div>
          </div>
          
          {/* Expanded Details */}
          {expandedMatch === index && (
            <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
              {/* Simplified details section for alternative matches */}
              <div className="space-y-2">
                {match.age && (
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Age</span>
                    <span className="font-medium text-gray-800 dark:text-gray-200">{match.age}</span>
                  </div>
                )}
                {match.abv && (
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">ABV</span>
                    <span className="font-medium text-gray-800 dark:text-gray-200">{match.abv}%</span>
                  </div>
                )}
                {match.fair_price && (
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Fair Price</span>
                    <span className="font-medium text-gray-800 dark:text-gray-200">{match.fair_price}</span>
                  </div>
                )}
                {match.shelf_price && (
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Shelf Price</span>
                    <span className="font-medium text-gray-800 dark:text-gray-200">{match.shelf_price}</span>
                  </div>
                )}
              </div>
              
              {/* Abbreviated tasting notes if available */}
              {match.tasting_notes && match.tasting_notes.nose && (
                <div className="mt-3 text-sm">
                  <span className="text-primary font-medium">Nose:</span>
                  <p className="text-gray-800 dark:text-gray-200 mt-1">
                    {match.tasting_notes.nose}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}