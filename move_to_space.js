const https = require('https');

const TOKEN = 'e3f36cb04f264e539e8d91b9a11fc8e2';

function callTool(toolName, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0',
      method: 'tools/call',
      params: { 
        name: toolName,
        arguments: params 
      },
      id: Date.now()
    });

    const options = {
      hostname: 'docs.qq.com',
      path: '/openapi/mcp',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': TOKEN,
        'Content-Length': Buffer.byteLength(body),
        'User-Agent': 'mcporter/1.0'
      }
    };

    const req = https.request(options, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { resolve({ raw: data }); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  // Move file to space
  console.log('Moving document to space...');
  const result = await callTool('manage.move_file_to_space', {
    file_id: 'DlFHFumOKbOg',
    space_id: 'DKPalbixlnEm'
  });
  console.log('Result:', JSON.stringify(result, null, 2));
}

main().catch(console.error);
