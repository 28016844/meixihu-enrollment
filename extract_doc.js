const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');

const docxPath = 'D:\\杨红\\梅溪湖小初高贯通培养 2026 暑假招生简章(1).docx';

try {
  const zip = new AdmZip(docxPath);
  const documentXml = zip.readAsText('word/document.xml');
  
  // Extract text from XML
  const textMatches = documentXml.match(/<w:t[^>]*>([^<]*)<\/w:t>/g) || [];
  const paragraphBreaks = documentXml.match(/<\/w:p>/g) || [];
  
  let result = '';
  let lastIndex = 0;
  
  // Simple extraction - get all text content
  const textContent = documentXml
    .replace(/<\/w:p>/g, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  
  // Better extraction using regex
  let texts = [];
  let currentPos = 0;
  const textRegex = /<w:t[^>]*>([^<]*)<\/w:t>/g;
  const pEndRegex = /<\/w:p>/g;
  
  // Build a map of positions
  const allMarkers = [];
  let match;
  
  while ((match = textRegex.exec(documentXml)) !== null) {
    allMarkers.push({ pos: match.index, type: 'text', text: match[1] });
  }
  
  while ((match = pEndRegex.exec(documentXml)) !== null) {
    allMarkers.push({ pos: match.index, type: 'newline' });
  }
  
  allMarkers.sort((a, b) => a.pos - b.pos);
  
  let output = '';
  for (const marker of allMarkers) {
    if (marker.type === 'text') {
      output += marker.text;
    } else {
      output += '\n';
    }
  }
  
  // Clean up multiple newlines
  output = output.replace(/\n{3,}/g, '\n\n');
  
  console.log(output);
} catch (err) {
  console.error('Error:', err.message);
}
