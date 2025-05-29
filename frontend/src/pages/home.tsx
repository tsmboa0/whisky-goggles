import { useState, useRef } from "react";
import { useLocation } from "wouter";
import Header from "@/components/header";
import UploadArea from "@/components/upload-area";
import ImagePreview from "@/components/image-preview";
import ScanningProgress from "@/components/scanning-progress";
import Camera from "@/components/camera";
import { useToast } from "@/hooks/use-toast";
import { scanWhiskyBottle } from "@/lib/api";

export default function Home() {
  const [location, setLocation] = useLocation();
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);
  const [showCamera, setShowCamera] = useState(false);
  const { toast } = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageSelected = (file: File) => {
    setSelectedImage(file);
    const imageUrl = URL.createObjectURL(file);
    setPreviewUrl(imageUrl);
  };

  const handleFileUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (!file.type.match('image.*')) {
        toast({
          title: "Invalid file type",
          description: "Please select an image file",
          variant: "destructive",
        });
        return;
      }
      handleImageSelected(file);
    }
  };

  const handleCameraCapture = () => {
    setShowCamera(true);
  };

  const handleCameraClose = () => {
    setShowCamera(false);
  };

  const handleCameraCaptureComplete = (file: File) => {
    setShowCamera(false);
    handleImageSelected(file);
  };

  // Track the scanning progress
  const handleScan = async () => {
    if (!selectedImage) {
      toast({
        title: "No image selected",
        description: "Please select or capture an image first",
        variant: "destructive",
      });
      return;
    }

    setIsScanning(true);
    setScanProgress(0);
    
    try {
      // Calculate duration to match the 4 second API delay
      const progressDuration = 4000; // 4 seconds
      const progressSteps = 20; // Number of steps to reach 100%
      const stepDelay = progressDuration / progressSteps;
      let currentProgress = 0;
      
      // Send image to backend for processing
      const formData = new FormData();
      formData.append("file", selectedImage);
      
      // Create a promise to handle the API request
      const apiRequest = fetch(`${window.location.origin}/recognize`, {
        method: 'POST',
        body: formData
      }).then(async (response) => {
        if (!response.ok) {
          throw new Error('Failed to scan the image');
        }
        return await response.json();
      });
      
      // Set up the progress interval
      const progressInterval = setInterval(() => {
        // Increment progress but keep it less than 95% until API completes
        if (currentProgress < 95) {
          currentProgress += 5;
          setScanProgress(currentProgress);
        }
      }, stepDelay);
      
      // // Wait for the API response
      const result = await apiRequest;
      console.log(`the response is: ${result}`)
      
      // // Clear the progress interval
      clearInterval(progressInterval);
      
      // // Store the result in sessionStorage
      sessionStorage.setItem("whiskyData", JSON.stringify(result));
      
      // // Set progress to 100% and redirect after a brief pause
      setScanProgress(100);
      
      // // Add a small delay before redirecting to ensure the 100% progress is visible
      setTimeout(() => {
        setIsScanning(false);
        setLocation("/results");
      }, 700);
      
    } catch (error) {
      console.error('Error:', error);
      setIsScanning(false);
      setScanProgress(0);
      toast({
        title: "Scan failed",
        description: "There was an error scanning the image. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen luxury-pattern dark:bg-gray-900">
      <div className="max-w-5xl mx-auto p-4 md:p-6">
        <Header />
        
        <main>
          <div className="luxury-card mb-8 dark:bg-gray-800 dark:border-gray-700">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-secondary dark:text-white">Discover Your Whisky</h2>
              <p className="text-gray-600 dark:text-gray-300 mt-2">Upload a photo of any whisky bottle to get detailed information</p>
            </div>

            {!previewUrl ? (
              <>
                <UploadArea onImageSelected={handleImageSelected} />
                
                <div className="flex flex-col sm:flex-row justify-center gap-6 mt-8">
                  <button 
                    onClick={handleCameraCapture}
                    className="burgundy-button flex items-center justify-center py-4 px-8 w-full sm:w-auto"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    Take Photo
                  </button>
                  
                  <button 
                    onClick={handleFileUploadClick}
                    className="gold-button flex items-center justify-center py-4 px-8 w-full sm:w-auto"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0l-4 4m4-4v12" />
                    </svg>
                    Upload Image
                  </button>
                </div>
                
                <input 
                  type="file" 
                  ref={fileInputRef}
                  className="hidden" 
                  accept="image/*" 
                  onChange={handleFileChange}
                />
              </>
            ) : (
              <div className="mt-8">
                <h3 className="text-xl font-semibold text-secondary mb-4">Image Preview</h3>
                
                <div className="bottle-container bg-gray-50 rounded-lg mb-4">
                  <ImagePreview 
                    imageUrl={previewUrl} 
                    isScanning={isScanning} 
                  />
                </div>
                
                {!isScanning ? (
                  <button 
                    onClick={handleScan}
                    className="gold-button w-full py-4 px-6 text-lg mt-6"
                  >
                    Scan Bottle
                  </button>
                ) : (
                  <ScanningProgress progress={scanProgress} />
                )}
              </div>
            )}
          </div>
          
          {showCamera && (
            <Camera
              onCapture={handleCameraCaptureComplete}
              onClose={handleCameraClose}
            />
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="luxury-card p-5 text-center dark:bg-gray-800 dark:border-gray-700">
              <div className="rounded-full bg-primary/10 dark:bg-primary/20 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">Snap a Photo</h3>
              <p className="text-gray-600 dark:text-gray-300">Take a clear photo of any whisky bottle label</p>
            </div>
            
            <div className="luxury-card p-5 text-center dark:bg-gray-800 dark:border-gray-700">
              <div className="rounded-full bg-primary/10 dark:bg-primary/20 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">Instant Analysis</h3>
              <p className="text-gray-600 dark:text-gray-300">Our AI identifies the bottle details instantly</p>
            </div>
            
            <div className="luxury-card p-5 text-center dark:bg-gray-800 dark:border-gray-700">
              <div className="rounded-full bg-primary/10 dark:bg-primary/20 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">Detailed Information</h3>
              <p className="text-gray-600 dark:text-gray-300">Get tasting notes, region, age and more</p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
