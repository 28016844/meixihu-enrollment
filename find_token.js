const fs = require('fs');
const path = require('path');
const os = require('os');

// Search for mcporter config files
const searchPaths = [
  path.join(os.homedir(), '.mcporter', 'config.json'),
  path.join(os.homedir(), '.config', 'mcporter', 'config.json'),
  path.join(process.env.APPDATA || '', 'mcporter', 'config.json'),
  path.join(process.env.LOCALAPPDATA || '', 'mcporter', 'config.json'),
  path.join(os.homedir(), '.openclaw', 'mcporter-config.json'),
  path.join(os.homedir(), '.openclaw', 'config', 'mcporter.json'),
  path.join('D:', 'Program Files', 'QClaw', 'resources', 'openclaw', 'config', 'skills', 'tencent-docs'),
];

for (const p of searchPaths) {
  if (fs.existsSync(p)) {
    console.log('Found:', p);
    try {
      const content = fs.readFileSync(p, 'utf8');
      if (p.endsWith('.json')) {
        console.log('Content:', content.substring(0, 500));
      } else {
        console.log('Files in dir:', fs.readdirSync(p));
      }
    } catch(e) {
      console.log('Read error:', e.message);
    }
    console.log('---');
  }
}

// Also search for any .env or token files
const home = os.homedir();
const dotFiles = ['.tencent_docs_token', '.tdoc_token', 'TENCENT_DOCS_TOKEN'];
for (const f of dotFiles) {
  const p = path.join(home, f);
  if (fs.existsSync(p)) {
    console.log('Token file:', p, fs.readFileSync(p, 'utf8').trim().substring(0, 50));
  }
}

// Check npm global config
try {
  const npmGlobal = execSync('npm root -g', {encoding:'utf8'}).trim();
  console.log('NPM global:', npmGlobal);
  const mcporterDir = path.join(npmGlobal, 'mcporter');
  if (fs.existsSync(mcporterDir)) {
    console.log('mcporter dir files:', fs.readdirSync(mcporterDir));
    const configPath = path.join(mcporterDir, 'config.json');
    if (fs.existsSync(configPath)) {
      console.log('Config:', fs.readFileSync(configPath, 'utf8').substring(0, 800));
    }
  }
} catch(e) {
  console.log('npm error:', e.message);
}
