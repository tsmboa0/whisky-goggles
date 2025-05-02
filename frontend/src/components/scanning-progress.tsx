import React from "react";
import { Progress } from "@/components/ui/progress";
import { CheckCircle2 } from "lucide-react";
import { useTheme } from "next-themes";

interface ScanningProgressProps {
  progress: number;
}

export default function ScanningProgress({ progress }: ScanningProgressProps) {
  const { theme } = useTheme();
  const isDark = theme === "dark";

  return (
    <div className="mt-6">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center">
          {progress < 100 ? (
            <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin mr-2"></div>
          ) : (
            <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" />
          )}
          <span className="font-medium text-gray-800 dark:text-white">
            {progress < 100 ? "Scanning image..." : "Scan complete!"}
          </span>
        </div>
        <span className="font-medium text-primary">{progress}%</span>
      </div>
      
      <Progress 
        value={progress} 
        className="h-3 bg-gray-100 dark:bg-gray-700" 
        style={{
          background: isDark 
            ? "linear-gradient(to right, #1f2937, #111827)" 
            : "linear-gradient(to right, #f3f4f6, #f9fafb)"
        }}
      />
      
      {progress === 100 && (
        <p className="mt-3 text-center text-sm text-gray-600 dark:text-gray-400">
          Redirecting to results...
        </p>
      )}
    </div>
  );
}
