const https = require('https');

const TOKEN = 'e3f36cb04f264e539e8d91b9a11fc8e2';
const SPACE_ID = 'DKPalbixlnEm';

function callTool(toolName, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0',
      method: toolName,
      params: { arguments: params },
      id: Date.now()
    });

    const options = {
      hostname: 'docs.qq.com',
      path: '/openapi/mcp',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + TOKEN,
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
  // Step 1: Create document in space
  console.log('Creating document in space...');
  const r1 = await callTool('create_space_node', {
    node_type: 'wiki_tdoc',
    space_id: SPACE_ID,
    title: '梅溪湖小初高贯通培养 2026 暑假招生简章',
    wiki_tdoc_node: {
      doc_type: 'smartcanvas',
      title: '梅溪湖小初高贯通培养 2026 暑假招生简章'
    }
  });
  console.log('Create result:', JSON.stringify(r1, null, 2));
}

main().catch(console.error);
