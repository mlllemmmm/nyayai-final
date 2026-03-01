import React, { useState, useRef, useEffect } from "react";

function VoiceHelp() {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  // Ref for the native audio element to play TTS response
  const audioPlayerRef = useRef(null);

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (
        mediaRecorderRef.current &&
        mediaRecorderRef.current.state === "recording"
      ) {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const handleStartRecording = async () => {
    try {
      setErrorMsg("");
      setTranscript("");
      setResponse("");
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        setIsProcessing(true);
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        await sendAudioToBase(audioBlob);
        
        // Stop all tracks to release mic
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Mic access denied or error:", err);
      setErrorMsg("Microphone access denied or unavailable. Please allow permissions.");
    }
  };

  const handleStopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendAudioToBase = async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      const res = await fetch("http://localhost:8000/api/voice-query", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Server responded with error.");
      }

      const data = await res.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      setTranscript(data.transcript);
      setResponse(data.text_response);

      if (data.audio_base64 && audioPlayerRef.current) {
        // Play the returned TTS audio
        const audioSrc = `data:audio/mp3;base64,${data.audio_base64}`;
        audioPlayerRef.current.src = audioSrc;
        audioPlayerRef.current.play().catch(e => console.error("Auto-play prevented", e));
      }
    } catch (err) {
      console.error("Error sending audio:", err);
      setErrorMsg("Failed to process audio. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="card voice-card">
      <h2>Voice Legal Help</h2>

      <div style={{ marginBottom: "20px" }}>
        {!isRecording ? (
          <button 
            className="mic-btn" 
            onClick={handleStartRecording}
            disabled={isProcessing}
            style={{ 
              fontSize: "2rem", 
              padding: "10px 20px", 
              cursor: isProcessing ? "not-allowed" : "pointer",
              backgroundColor: isProcessing ? "#ccc" : "#007bff",
              color: "white",
              borderRadius: "50%",
              border: "none",
              width: "80px",
              height: "80px"
            }}
          >
            🎤
          </button>
        ) : (
          <button 
            className="mic-btn recording" 
            onClick={handleStopRecording}
            style={{ 
              fontSize: "2rem", 
              padding: "10px 20px", 
              cursor: "pointer",
              backgroundColor: "#ff4d4f",
              color: "white",
              borderRadius: "50%",
              border: "none",
              width: "80px",
              height: "80px",
              animation: "pulse 1.5s infinite"
            }}
          >
            ⏹️
          </button>
        )}
      </div>

      <p>
        {isRecording ? "Listening..." : isProcessing ? "Processing..." : "Tap to Speak"}
      </p>

      {errorMsg && (
        <div style={{ color: "red", marginTop: "10px" }}>
          {errorMsg}
        </div>
      )}

      {transcript && (
        <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#f0f2f5", borderRadius: "8px", textAlign: "left" }}>
          <strong>You said:</strong> <br />
          <em>"{transcript}"</em>
        </div>
      )}

      <div className="response" style={{ marginTop: "20px", textAlign: "left" }}>
        {response ? (
          <div>
            <strong>NyayAI:</strong> <br />
            {response}
          </div>
        ) : (
          <p style={{ color: "#888" }}>Voice response will appear here...</p>
        )}
      </div>

      {/* Hidden audio element for playback */}
      <audio ref={audioPlayerRef} style={{ display: "none" }} />
    </div>
  );
}

export default VoiceHelp;
