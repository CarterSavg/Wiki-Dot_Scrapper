import { useState } from 'react';
import './LoadingIcon.css';
import loadingIcon from '../../assets/Book.webm';


function LoadingIcon() {
  return (
    <div className="loading-book">
        <video className ="loading-video" width="300" height="300" autoPlay loop muted playsInline>
            <source src={loadingIcon} type="video/webm" />
      </video>
    </div>
  )
}

export default LoadingIcon;