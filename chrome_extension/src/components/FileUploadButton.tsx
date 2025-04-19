import React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

// Hide the default input and style a custom button
const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

interface FileUploadInputProps {
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  fileName?: string;
  accept?: string;
  required?: boolean;
}

const FileUploadInput: React.FC<FileUploadInputProps> = ({
  onChange,
  fileName,
  accept = ".pdf,.doc,.docx",
  required = false
}) => {
  return (
    <div className="mt-1">
      <Button
        component="label"
        variant="contained"
        startIcon={<CloudUploadIcon />}
        className="bg-blue-600 hover:bg-blue-700 normal-case"
      >
        {fileName ? 'Change File' : 'Choose File'}
        <VisuallyHiddenInput 
          type="file" 
          onChange={onChange} 
          accept={accept}
          required={required}
        />
      </Button>
      {fileName && (
        <span className="ml-3 text-sm text-gray-600 truncate max-w-xs inline-block">
          {fileName}
        </span>
      )}
    </div>
  );
};

export default FileUploadInput;
