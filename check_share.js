const https = require('https');

const TOKEN = 'e3f36cb04f264e539e8d91b9a11fc8e2';
const FILE_ID = 'DpxVtqiLiCqz';

function callTool(toolName, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0',
      method: 'tools/call',
      params: { name: toolName, arguments: params },
      id: Date.now()
    });

    const options = {
      hostname: 'docs.qq.com',
      path: '/openapi/mcp',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': TOKEN,
        'Content-Length': Buffer.byteLength(body)
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
  // Check current sharing info
  console.log('Getting file info...');
  const info = await callTool('manage.query_file_info', { file_id: FILE_ID });
  console.log('File info:', JSON.stringify(info, null, 2));

  // Get privilege
  console.log('\nGetting privilege...');
  const priv = await callTool('manage.get_privilege', { file_id: FILE_ID });
  console.log('Privilege:', JSON.stringify(priv, null, 2));

  // Get recent online files
  console.log('\nGetting recent files...');
  const recent = await callTool('manage.recent_online_file', {});
  console.log('Recent files:', JSON.stringify(recent, null, 2));
}

main().catch(console.error);
