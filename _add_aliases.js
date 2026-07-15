const fs = require('fs');

// 1. Parse all entries from list.yaml with full line content
const raw = fs.readFileSync('src/_meta/list.yaml', 'utf-8').replace(/\r/g, '');
const lines = raw.split('\n');

// 2. Split into entry blocks (key line + its content until next key)
const entryBlocks = []; // { key, name, aliases[], textLines[] }
let currentKey = null;
let currentName = '';
let currentAliases = [];
let currentLines = [];

function flushEntry() {
  if (currentKey) {
    entryBlocks.push({
      key: currentKey,
      name: currentName,
      aliases: [...currentAliases],
      lines: [...currentLines]
    });
  }
}

for (let i = 0; i < lines.length; i++) {
  const t = lines[i].trim();
  const km = lines[i].match(/^([a-zA-Z0-9_][\w\-]*):\s*$/);
  if (km) {
    flushEntry();
    currentKey = km[1];
    currentName = '';
    currentAliases = [];
    currentLines = [lines[i]];
    continue;
  }
  if (currentKey) {
    currentLines.push(lines[i]);
    if (t.startsWith('name:')) {
      currentName = t.substring(5).trim().replace(/^['"]|['"]$/g, '');
    }
    if (lines[i].match(/^\s{4}-\s/)) {
      const v = t.replace(/^-\s*/, '').replace(/^['"]|['"]$/g, '');
      if (v && !v.includes(':')) currentAliases.push(v);
    }
  }
}
flushEntry();

// 3. Build lookup: any known name -> key
const lookup = {};
for (const e of entryBlocks) {
  lookup[e.key.toLowerCase()] = e.key;
  lookup[e.name.toLowerCase()] = e.key;
  for (const a of e.aliases) lookup[a.toLowerCase()] = e.key;
}

// 4. All alias mappings
const mappings = [
  ['mina0977', ['bebe']],
  ['TS', ['蓓蓓酱']],
  ['CathyBBlove', ['cmbprod']],
  ['LunaRodriguezMonteroLunaTrapLunaRM', ['Luna Trap Luna RM']],
  ['Chengxinglin', ['星セリ', '金城りせ']],
  ['YukoMomohi', ['君野ここ', 'Yuko Momohi']],
  ['miso1239', ['李熙', '이소희', 'Lee So-hee-II', 'live E소희']],
  ['Yueya', ['性感电臀女王']],
  ['kyl1012', ['진서', '青草']],
  ['klive19101403', ['은소라', '손예은', '孙乐乐', '孫樂樂', 'SonYe-Eun']],
  ['gggg90', ['live Subin']],
  ['KimHaNeulHyena', ['Kim Ha Neul']],
  ['Hyena', ['정혜나']],
  ['Seulbi', ['슬비']],
  ['Yaomeinvwanghulijing', ['妲己专职勾引']],
  ['JJiongwltn9818winktv', ['JJiong']],
  ['Apple', ['苹果']],
  ['xxs2xxx', ['SeolHui']],
  ['carpediem110392winktv', ['崔黛恩', '黛恩娜']],
  ['Erciyuankuangreshaonv', ['甜甜圈']],
  ['lovable33AfreecaTV', ['다희', '韩国主播圆圆', '탱글다희']],
  ['00', ['00后超级凶', '00后超级胸']],
  ['nanacute', ['大啵啵', '大波波', 'mbbong']],
  ['Anna', ['玉兔兔', '安娜Anna']],
  ['Naiyoumeimei', ['小卓']],
  ['Yiman', ['英熙', '在熙']],
  ['5721004', ['오지림']],
  ['wkdus222', ['洛思']],
  ['Gaoyinxing', ['고은별']],
  ['NAGISANagesa', ['Nagesa小清']],
  ['LINABUBUJKF', ['布布']],
  ['Buchunxuemei', ['树屋灵灵']],
  ['Dongbeiyanzhixuesheng', ['炉果']],
  ['Wangdapao', ['卯卯', '卯哥', '相声演员的自我修养', '卯卯少女']],
  ['Nanbeibei', ['葱姜蒜', '西东东', '真的好温柔']],
  ['OkitaMisuzu', ['Okita Misuzu']],
  ['Xirui', ['性感黛西', '小崽崽']],
  ['baby', ['茜宝', '西宝']],
  ['SandyCoco', ['Sandy Coco', '蔡欣蓓']],
  ['MikiWu20EGirls', ['Miki Wu']],
  ['AlleyBella', ['Alley', '錢昱慈']],
  ['izayoiRui', ['十六夜涙']],
  ['smoneyordieonlyfansSkyBri', ['Sky Bri']],
  ['lyainevan', ['@lyainevan']],
  ['cookiemon18', ['น้องคุกกี้ กลุ่มลับน้องคุกกี้']],
  ['SeoaliveDodo', ['Seoa', 'live Dodo']],
  ['Zizixi', ['小露西西']],
  ['Xiaojian', ['一只可爱简']],
  ['Yinanna', ['余小c']],
  ['LisaOkko', ['Lisa Okko']],
  ['FantasyFactory', ['Fantasy Factory']],
  ['YeonWoo', ['Yeon Woo']],
  ['Chuanyunyin', ['妙妙音']],
  ['Palisi', ['瑞瑞']],
  ['Shengyouxiaomeimo', ['小恶龙']],
  ['CarlaGrace', ['Carla Grace']],
  ['ArisaraKarbdecho', ['Arisara Karbdecho']],
  ['JoeyChua', ['Joey Chua']],
  ['ChoiSeolhwa', ['최설화']],
  ['Pyoeunji', ['朴恩智']],
  ['FaiiOrapunPitta', ['Pitta']],
  ['GirlCrush', ['Bomi']],
  ['Linxingmei', ['임성미']],
  ['Liushifei', ['류세비']],
  ['Pujilan', ['박기량']],
  ['SongJooA', ['송주아', 'Song JooA']],
  ['Xuanzi', ['顾桥楠']],
  ['SeoRina', ['서리나']],
  ['ShinSaeRom', ['신새롬']],
  ['PorimaCheng', ['Porima Cheng']],
  ['Candy', ['Candy糖糖']],
  ['LolitaCheng', ['Lolita Cheng']],
  ['Zhaoningning', ['小隋棠']],
  ['TuangratChatsathavorn', ['ตวงรัตน์ ชาติสถาวร']],
  ['Xiaxiyao', ['潘霜霜']],
];

// 5. Build set of new aliases per entry key
const newAliasesMap = {}; // key -> string[]
let errors = 0;

for (const [ref, aliases] of mappings) {
  const key = lookup[ref.toLowerCase()];
  if (!key) { console.log('ERROR: "' + ref + '" not found'); errors++; continue; }
  const existingSet = new Set(entryBlocks.find(e => e.key === key).aliases.map(a => a.toLowerCase()));
  if (!newAliasesMap[key]) newAliasesMap[key] = [];
  for (const al of aliases) {
    if (!existingSet.has(al.toLowerCase())) newAliasesMap[key].push(al);
  }
}

console.log('Entries to update: ' + Object.keys(newAliasesMap).length + ' (errors: ' + errors + ')\n');

// 6. Generate output by processing entry blocks in order
const outLines = [];

for (const block of entryBlocks) {
  const newAliases = newAliasesMap[block.key];
  if (!newAliases || newAliases.length === 0) {
    // No changes — just write as-is
    for (const l of block.lines) outLines.push(l);
    console.log('  ' + block.key + ': no change');
    continue;
  }

  // Find where to insert: after name: line, or after last existing alias
  let insertIdx = -1;
  let hasAliases = false;

  for (let i = 0; i < block.lines.length; i++) {
    if (block.lines[i].trim() === 'aliases:') {
      hasAliases = true;
      let j = i + 1;
      while (j < block.lines.length && block.lines[j].match(/^\s{4}- /)) j++;
      insertIdx = j;
      break;
    }
  }
  if (!hasAliases) {
    for (let i = 0; i < block.lines.length; i++) {
      if (block.lines[i].trim().startsWith('name:')) {
        insertIdx = i + 1;
        break;
      }
    }
  }

  if (insertIdx < 0) {
    console.log('FAIL: cannot find insert position for ' + block.key);
    for (const l of block.lines) outLines.push(l);
    continue;
  }

  // Build new lines for this entry
  const before = block.lines.slice(0, insertIdx);
  const after = block.lines.slice(insertIdx);
  const insert = hasAliases
    ? newAliases.map(a => '  - ' + a)
    : ['  aliases:', ...newAliases.map(a => '  - ' + a)];

  for (const l of before) outLines.push(l);
  for (const l of insert) outLines.push(l);
  for (const l of after) outLines.push(l);
  console.log('  ' + block.key + ': +' + newAliases.length + ' aliases');
}

// 7. Write output
fs.writeFileSync('src/_meta/list.yaml', outLines.join('\n'), 'utf-8');
console.log('\nDone! ' + outLines.length + ' lines written.');
