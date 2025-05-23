import React, { useState } from 'react';
import DescriptionIcon from '@mui/icons-material/Description';
import { getUserEmail } from '../chrome/utils';
import { Button } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import FileUploadInput from './FileUploadButton';

function UploadResume() {
  const [resume, setResume] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setResume(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    if (!resume) {
      setError('Please provide both your resume file.');
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append('resume', resume);
    formData.append('userId', await getUserEmail());

    try {
      const response = await fetch('http://127.0.0.1:8080/upload/upload-resume', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed.');
      }
      setSuccess(true);
      setResume(null);
    } catch (err) {
      setError('An error occurred while uploading. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-6 pt-12">
      <DescriptionIcon className="w-64 h-64 text-gray-400" />
      <div className="text-center space-y-2">
        <h1 className="text-xl font-semibold text-gray-900">
          Upload your resume.
        </h1>
        <p className="text-gray-600">
          By uploading your resume, we can tailor your results to your work history.
        </p>
      </div>
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <div>
          <label className="block text-gray-700">Resume</label>
          <FileUploadInput
            onChange={handleFileChange}
            fileName={resume?.name}
            accept=".pdf,.doc,.docx"
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            Accepted formats: PDF, DOC, DOCX
          </p>
        </div>
        {error && <p className="text-red-500">{error}</p>}
        {success && <p className="text-green-500">Resume uploaded successfully!</p>}
        <Button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg"
          startIcon={<CloudUploadIcon />}
          disabled={loading}
        >
          {loading ? 'Uploading...' : 'Upload Resume'}
        </Button>
      </form>
    </div>
  );
}

export default UploadResume;
