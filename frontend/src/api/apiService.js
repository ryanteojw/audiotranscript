let rootURL = "http://localhost:5000"

export const getHealthStatus = rootURL + "/health"
export const getAllTranscriptions = rootURL + "/transcriptions"
export const createAudioTranscribe = rootURL + "/transcribe"
export const getFilteredAudioData = rootURL + "/search"