import React, { useState, useRef, useEffect } from "react";

function VoiceHelp() {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioPlayerRef = useRef(null);

  useEffect(() => {
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
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });
        await sendAudioToBase(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error(err);
      setErrorMsg(
        "Microphone access denied or unavailable. Please allow permissions."
      );
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

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();

      setTranscript(data.transcript);
      setResponse(data.text_response);

      if (data.audio_base64 && audioPlayerRef.current) {
        audioPlayerRef.current.src = `data:audio/mp3;base64,${data.audio_base64}`;
        audioPlayerRef.current.play();
      }
    } catch (err) {
      console.error(err);
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
          >
            🎤
          </button>
        ) : (
          <button
            className="mic-btn recording"
            onClick={handleStopRecording}
          >
            ⏹️
          </button>
        )}
      </div>

      <p>
        {isRecording
          ? "Listening..."
          : isProcessing
          ? "Processing..."
          : "Tap to Speak"}
      </p>

      {errorMsg && <div style={{ color: "red" }}>{errorMsg}</div>}

      {transcript && (
        <div>
          <strong>You said:</strong> <em>"{transcript}"</em>
        </div>
      )}

      <div className="response">
        {response ? (
          <>
            <strong>NyayAI:</strong>
            <p>{response}</p>
          </>
        ) : (
          <p>Voice response will appear here...</p>
        )}
      </div>

      <audio ref={audioPlayerRef} style={{ display: "none" }} />
    </div>
  );
}

export default VoiceHelp;