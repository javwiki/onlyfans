const fs = require('fs');

function loadProjectEntries() {
  const text = fs.readFileSync('src/_meta/list.yaml', 'utf-8').replace(/\r/g, '');
  const lines = text.split('\n');
  const entries = {};
  let currentKey = null;
  let currentStart = null;
  let currentName = '';
  let currentAliases = [];

  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    const keyMatch = lines[i].match(/^([a-zA-Z0-9_][\w\-]*):\s*$/);
    if (keyMatch) {
      if (currentKey) entries[currentKey] = { startLine: currentStart, name: currentName, aliases: [...currentAliases] };
      currentKey = keyMatch[1];
      currentStart = i;
      currentName = '';
      currentAliases = [];
      continue;
    }
    if (currentKey && trimmed.startsWith('name:'))
      currentName = trimmed.substring(5).trim().replace(/^['"]|['"]$/g, '');
    if (currentKey && lines[i].match(/^\s{4}-\s/)) {
      const val = trimmed.replace(/^-\s*/, '').replace(/^['"]|['"]$/g, '');
      if (val && !val.includes(':')) currentAliases.push(val);
    }
  }
  if (currentKey) entries[currentKey] = { startLine: currentStart, name: currentName, aliases: [...currentAliases] };

  // Build entries in file order
  const ordered = [];
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^([a-zA-Z0-9_][\w\-]*):\s*$/);
    if (m && entries[m[1]]) ordered.push(m[1]);
  }
  return { entries, lines, ordered };
}

// Build nameToKey
function buildNameToKey(entries) {
  const map = {};
  for (const [key, entry] of Object.entries(entries)) {
    map[key.toLowerCase()] = key;
    map[entry.name.toLowerCase()] = key;
    for (const a of entry.aliases) map[a.toLowerCase()] = key;
  }
  return map;
}

const { entries, lines, ordered } = loadProjectEntries();
const nameToKey = buildNameToKey(entries);

function addAlias(existing, newAlias) {
  const key = nameToKey[existing.toLowerCase()];
  if (!key) { console.log("  NOT FOUND: " + existing); return; }
  const existingAliasesLower = entries[key].aliases.map(a => a.toLowerCase());
  if (existingAliasesLower.includes(newAlias.toLowerCase())) return;
  if (!entries[key]._newAliases) entries[key]._newAliases = [];
  entries[key]._newAliases.push(newAlias);
}

addAlias('mina0977', 'bebe');
addAlias('TS', '蓓蓓酱');
addAlias('CathyBBlove', 'cmbprod');
addAlias('LunaRodriguezMonteroLunaTrapLunaRM', 'Luna Trap Luna RM');
addAlias('Chengxinglin', '星セリ');
addAlias('Chengxinglin', '金城りせ');
addAlias('YukoMomohi', '君野ここ');
addAlias('YukoMomohi', 'Yuko Momohi');
addAlias('miso1239', '李熙');
addAlias('miso1239', '이소희');
addAlias('miso1239', 'Lee So-hee-II');
addAlias('miso1239', 'live E소희');
addAlias('Yueya', '性感电臀女王');
addAlias('kyl1012', '진서');
addAlias('kyl1012', '青草');
addAlias('klive19101403', '은소라');
addAlias('klive19101403', '손예은');
addAlias('klive19101403', '孙乐乐');
addAlias('klive19101403', '孫樂樂');
addAlias('klive19101403', 'SonYe-Eun');
addAlias('gggg90', 'live Subin');
addAlias('KimHaNeulHyena', 'Kim Ha Neul');
addAlias('Hyena', '정혜나');
addAlias('Seulbi', '슬비');
addAlias('Yaomeinvwanghulijing', '妲己专职勾引');
addAlias('JJiongwltn9818winktv', 'JJiong');
addAlias('Apple', '苹果');
addAlias('xxs2xxx', 'SeolHui');
addAlias('carpediem110392winktv', '崔黛恩');
addAlias('carpediem110392winktv', '黛恩娜');
addAlias('Erciyuankuangreshaonv', '甜甜圈');
addAlias('lovable33AfreecaTV', '다희');
addAlias('lovable33AfreecaTV', '韩国主播圆圆');
addAlias('lovable33AfreecaTV', '탱글다희');
addAlias('00', '00后超级凶');
addAlias('00', '00后超级胸');
addAlias('nanacute', '大啵啵');
addAlias('nanacute', '大波波');
addAlias('nanacute', 'mbbong');
addAlias('Anna', '玉兔兔');
addAlias('Anna', '安娜Anna');
addAlias('Naiyoumeimei', '小卓');
addAlias('Yiman', '英熙');
addAlias('Yiman', '在熙');
addAlias('5721004', '오지림');
addAlias('wkdus222', '洛思');
addAlias('Gaoyinxing', '고은별');
addAlias('NAGISANagesa', 'Nagesa小清');
addAlias('LINABUBUJKF', '布布');
addAlias('Buchunxuemei', '树屋灵灵');
addAlias('Dongbeiyanzhixuesheng', '炉果');
addAlias('Wangdapao', '卯卯');
addAlias('Wangdapao', '卯哥');
addAlias('Wangdapao', '相声演员的自我修养');
addAlias('Wangdapao', '卯卯少女');
addAlias('Nanbeibei', '葱姜蒜');
addAlias('Nanbeibei', '西东东');
addAlias('Nanbeibei', '真的好温柔');
addAlias('OkitaMisuzu', 'Okita Misuzu');
addAlias('Xirui', '性感黛西');
addAlias('Xirui', '小崽崽');
addAlias('baby', '茜宝');
addAlias('baby', '西宝');
addAlias('SandyCoco', 'Sandy Coco');
addAlias('SandyCoco', '蔡欣蓓');
addAlias('MikiWu20EGirls', 'Miki Wu');
addAlias('AlleyBella', 'Alley');
addAlias('AlleyBella', '錢昱慈');
addAlias('izayoiRui', '十六夜涙');
addAlias('smoneyordieonlyfansSkyBri', 'Sky Bri');
addAlias('lyainevan', '@lyainevan');
addAlias('cookiemon18', 'น้องคุกกี้ กลุ่มลับน้องคุกกี้');
addAlias('SeoaliveDodo', 'Seoa');
addAlias('SeoaliveDodo', 'live Dodo');
addAlias('Zizixi', '小露西西');
addAlias('Xiaojian', '一只可爱简');
addAlias('Yinanna', '余小c');
addAlias('LisaOkko', 'Lisa Okko');
addAlias('FantasyFactory', 'Fantasy Factory');
addAlias('YeonWoo', 'Yeon Woo');
addAlias('Chuanyunyin', '妙妙音');
addAlias('Palisi', '瑞瑞');
addAlias('Shengyouxiaomeimo', '小恶龙');
addAlias('CarlaGrace', 'Carla Grace');
addAlias('ArisaraKarbdecho', 'Arisara Karbdecho');
addAlias('JoeyChua', 'Joey Chua');
addAlias('ChoiSeolhwa', '최설화');
addAlias('Pyoeunji', '朴恩智');
addAlias('FaiiOrapunPitta', 'Pitta');
addAlias('GirlCrush', 'Bomi');
addAlias('Linxingmei', '임성미');
addAlias('Liushifei', '류세비');
addAlias('Pujilan', '박기량');
addAlias('SongJooA', '송주아');
addAlias('SongJooA', 'Song JooA');
addAlias('Xuanzi', '顾桥楠');
addAlias('SeoRina', '서리나');
addAlias('ShinSaeRom', '신새롬');
addAlias('PorimaCheng', 'Porima Cheng');
addAlias('Candy', 'Candy糖糖');
addAlias('LolitaCheng', 'Lolita Cheng');
addAlias('Zhaoningning', '小隋棠');
addAlias('TuangratChatsathavorn', 'ตวงรัตน์ ชาติสถาวร');
addAlias('Xiaxiyao', '潘霜霜');

// Process entries in REVERSE file order
let newLines = [...lines];
let offset = 0;

for (let idx = ordered.length - 1; idx >= 0; idx--) {
  const key = ordered[idx];
  const entry = entries[key];
  if (!entry._newAliases || entry._newAliases.length === 0) continue;

  // Find the actual line in (possibly modified) newLines
  let actualStart = -1;
  for (let i = entry.startLine; i < entry.startLine + 10; i++) {
    if (newLines[i] && newLines[i].trim() === key + ':') {
      actualStart = i;
      break;
    }
  }
  if (actualStart < 0) {
    console.log("  WARNING: cannot find key line for " + key);
    continue;
  }

  // Search for aliases or name:
  let insertPos = -1;
  let hasAliases = false;
  let searchEnd = Math.min(actualStart + 20, newLines.length);
  for (let i = actualStart; i < searchEnd; i++) {
    if (newLines[i].trim().startsWith('aliases:')) {
      hasAliases = true;
      let j = i + 1;
      while (j < searchEnd && newLines[j].match(/^\s{4}- /)) j++;
      insertPos = j;
      break;
    }
  }
  if (!hasAliases) {
    for (let i = actualStart; i < searchEnd; i++) {
      if (newLines[i].trim().startsWith('name:')) {
        insertPos = i + 1;
        break;
      }
    }
  }

  if (insertPos < 0) {
    console.log("  FAIL: cannot find insert pos for " + key);
    continue;
  }

  const aliasLines = hasAliases
    ? entry._newAliases.map(a => "  - " + a)
    : ["  aliases:", ...entry._newAliases.map(a => "  - " + a)];

  newLines.splice(insertPos, 0, ...aliasLines);
  console.log("  " + key + ": +" + entry._newAliases.length + " aliases");
}

fs.writeFileSync('src/_meta/list.yaml', newLines.join('\n'), 'utf-8');
console.log("\nDone! list.yaml updated.");
