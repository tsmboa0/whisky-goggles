import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

interface UploadAreaProps {
  onImageSelected: (file: File) => void;
}

export default function UploadArea({ onImageSelected }: UploadAreaProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onImageSelected(acceptedFiles[0]);
      }
    },
    [onImageSelected]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": []
    },
    maxFiles: 1,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all ${
        isDragActive 
          ? "border-primary bg-primary/5 dark:bg-primary/10" 
          : "border-gray-200 dark:border-gray-600 hover:border-primary hover:bg-primary/5 dark:hover:bg-primary/10"
      }`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center justify-center">
        <div className="w-20 h-20 rounded-full bg-primary/10 dark:bg-primary/20 flex items-center justify-center mb-5">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-10 w-10 text-primary"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        <p className="text-gray-800 dark:text-white font-medium text-lg mb-2">
          {isDragActive
            ? "Drop your whisky bottle image here"
            : "Drag & drop your whisky bottle image here"}
        </p>
        <p className="text-gray-500 dark:text-gray-400">
          {isDragActive 
            ? "Release to upload" 
            : "or select an option below for instant identification"}
        </p>
      </div>
    </div>
  );
}
