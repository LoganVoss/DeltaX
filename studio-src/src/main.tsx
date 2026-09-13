import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { ChampagneStudio } from '@/components/champagne-studio';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ChampagneStudio />
  </StrictMode>,
);
