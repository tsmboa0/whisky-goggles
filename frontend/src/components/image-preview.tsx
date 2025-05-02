import React from "react";

interface ImagePreviewProps {
  imageUrl: string;
  isScanning: boolean;
}

export default function ImagePreview({ imageUrl, isScanning }: ImagePreviewProps) {
  return (
    <div className="relative w-full h-full">
      <img
        src={imageUrl}
        alt="Whisky bottle preview"
        className="w-full h-full object-contain"
      />
      
      {isScanning && (
        <div className="absolute inset-0 bg-black bg-opacity-20">
          <div className="absolute top-0 left-0 right-0 h-1.5 bg-primary opacity-80 shadow-lg scan-line"></div>
        </div>
      )}
    </div>
  );
}
