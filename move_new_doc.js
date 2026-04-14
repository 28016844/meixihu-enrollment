const https = require('https');

const TOKEN = 'e3f36cb04f264e539e8d91b9a11fc8e2';
const FILE_ID = 'DpxVtqiLiCqz';
const SPACE_ID = 'DKPalbixlnEm';

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
  // Set to public
  console.log('Setting document to public...');
  const privResult = await callTool('manage.set_privilege', {
    file_id: FILE_ID,
    policy: 2
  });
  console.log('Privilege result:', JSON.stringify(privResult, null, 2));
  
  // Move to space
  console.log('\nMoving document to space...');
  const moveResult = await callTool('manage.move_file_to_space', {
    file_id: FILE_ID,
    space_id: SPACE_ID
  });
  console.log('Move result:', JSON.stringify(moveResult, null, 2));
  
  console.log('\n✅ Done! New document URL: https://docs.qq.com/aio/DRHB4VnRxaUxpQ3F6');
}

main().catch(console.error);
