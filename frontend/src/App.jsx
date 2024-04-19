import React, { useState, useRef } from 'react';
import tw from 'tailwind-styled-components';
import { FiMic, FiMicOff } from 'react-icons/fi';

const Container = tw.div`
  flex flex-col items-center justify-center h-screen bg-gray-100
`;

const VideoContainer = tw.div`
  relative w-1/2 rounded-lg overflow-hidden shadow-lg bg-gray-900
`;

const Video = tw.video`
  w-full h-auto
`;

const Button = tw.button`
  mt-4 px-6 py-3 bg-blue-600 text-white rounded-md shadow-md flex items-center justify-center space-x-2
  hover:bg-blue-700
`;

const Input = tw.input`
  mt-4 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500
`;

const AudioRecorder = () => {
  const [stream, setStream] = useState(null);
  const [recording, setRecording] = useState(false);
  const [username, setUsername] = useState('');
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);

  const startRecording = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: true });
      setStream(mediaStream);
      const recorder = new MediaRecorder(mediaStream);
      recorder.ondataavailable = (e) => {
        chunks.current.push(e.data);
      };
      recorder.onstop = () => {
        const audioBlob = new Blob(chunks.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(audioBlob);
        const a = document.createElement('a');
        document.body.appendChild(a);
        a.style = 'display: none';
        a.href = url;
        a.download = `${username}_audio_recording.wav`;
        a.click();
        window.URL.revokeObjectURL(url);
        chunks.current = [];
        setRecording(false);
        setStream(null);
      };
      recorder.start();
      mediaRecorder.current = recorder;
      setRecording(true);
    } catch (error) {
      console.error('Error accessing microphone and camera:', error);
    }
  };

  const stopRecording = () => {
    mediaRecorder.current.stop();
  };

  return (
    <Container>
      <Input
        type="text"
        placeholder="Enter your name"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="w-1/2"
      />
      <VideoContainer>
        {stream && <Video autoPlay playsInline muted ref={(video) => (video.srcObject = stream)} />}
      </VideoContainer>
      <Button onClick={recording ? stopRecording : startRecording}>
        {recording ? <FiMic size={24} /> : <FiMicOff size={24} />}
        <span>{recording ? 'Stop Recording' : 'Start Recording'}</span>
      </Button>
    </Container>
  );
};

export default AudioRecorder;
