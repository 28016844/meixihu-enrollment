const { execSync, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const skillDir = 'D:/Program Files/QClaw/resources/openclaw/config/skills/tencent-docs';

// Read auth token
let token = '';
try {
  const configPath = path.join(process.env.APPDATA || '', 'mcporter', 'config.json');
  if (fs.existsSync(configPath)) {
    const cfg = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const tdoc = cfg.servers?.tencent_docs || cfg.tencent_docs;
    if (tdoc?.headers) {
      const auth = tdoc.headers['Authorization'] || tdoc.headers['authorization'];
      if (auth) token = auth.replace('Bearer ', '').replace('Token ', '');
    }
  }
} catch(e) {}

// Also check env
if (!token) token = process.env.TENCENT_DOCS_TOKEN || '';

console.log('Token found:', token ? 'YES (length=' + token.length + ')' : 'NO');

// Try direct HTTP call to the MCP endpoint
async function callMCP(toolName, args) {
  const endpoint = 'https://docs.qq.com/openapi/mcp';
  const body = JSON.stringify({
    jsonrpc: '2.0',
    method: toolName,
    params: { arguments: args },
    id: Date.now()
  });

  // Use node http module
  const https = require('https');
  const urlObj = new URL(endpoint);

  const options = {
    hostname: urlObj.hostname,
    path: urlObj.pathname,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token.startsWith('eyJ') ? 'Bearer ' + token : 'Token ' + token,
      'User-Agent': 'mcporter/0.8.1'
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => resolve({ status: res.statusCode, data }));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  try {
    const r = await callMCP('create_space', { title: '梅溪湖招生简章' });
    console.log('Status:', r.status);
    console.log('Response:', r.data);
  } catch(e) {
    console.error('Error:', e.message);
  }
}

main();
