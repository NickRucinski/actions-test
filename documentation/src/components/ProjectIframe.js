import React from 'react';

function ProjectIframe({ docFolder }) {
  const projectName = process.env.PROJECT_NAME || 'docs-dev-mode'; // Fallback
  const iframeSrc = `/${projectName}/${docFolder}/index.html`; // Your iframe source

  return (
    <a href={iframeSrc} target="_blank" rel="noopener noreferrer">
      Click to see a full screen view
      <iframe src={iframeSrc} width="100%" height="600px" title="Project Documentation" />
    </a>
  );
}

export default ProjectIframe;
