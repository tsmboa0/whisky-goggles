import { apiRequest } from "@/lib/queryClient";
import { WhiskyData } from "@/types/whisky";

/**
 * Sends an image to the backend for whisky bottle detection and analysis
 * @param formData - FormData containing the image file
 * @returns Whisky data object with details about the detected bottle
 */
export async function scanWhiskyBottle(formData: FormData): Promise<WhiskyData> {
  try {
    const response = await apiRequest("POST", "/api/scan", formData);
    return await response.json();
  } catch (error) {
    console.error("Error scanning whisky bottle:", error);
    throw error;
  }
}
