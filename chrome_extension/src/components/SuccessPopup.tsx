import React from 'react';
import { Snackbar, Alert, AlertProps, Zoom } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { styled, keyframes } from '@mui/system';

interface SuccessPopupProps {
  open: boolean;
  message: string;
  onClose: () => void;
  duration?: number;
}

// Create a check mark animation
const checkmarkAnimation = keyframes`
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
`;

const AnimatedCheckIcon = styled(CheckCircleOutlineIcon)`
  animation: ${checkmarkAnimation} 0.5s ease-out forwards;
`;

const StyledAlert = styled(Alert)<AlertProps>(({ theme }) => ({
  alignItems: 'center',
  borderRadius: 10,
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
  '& .MuiAlert-icon': {
    fontSize: 22,
    padding: 0,
  },
  '& .MuiAlert-message': {
    fontSize: 16,
    fontWeight: 500,
  },
}));

const SuccessPopup: React.FC<SuccessPopupProps> = ({ 
  open, 
  message, 
  onClose, 
  duration = 5000 
}) => {
  return (
    <Snackbar
      open={open}
      autoHideDuration={duration}
      onClose={onClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      TransitionComponent={Zoom}
      sx={{
        marginTop: '24px',
      }}
    >
      <StyledAlert
        icon={<AnimatedCheckIcon />}
        variant="filled"
        severity="success"
        onClose={onClose}
      >
        {message}
      </StyledAlert>
    </Snackbar>
  );
};

export default SuccessPopup;
