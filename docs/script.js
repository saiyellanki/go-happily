const QUOTES = [
  ["You have power over your mind — not outside events. Realize this, and you will find strength.", "Marcus Aurelius"],
  ["Waste no more time arguing about what a good person should be. Be one.", "Marcus Aurelius"],
  ["The present moment is all you ever have.", "Traditional wisdom"],
];

function init(){
  window.historyData = JSON.parse(localStorage.getItem('gohappily_history')||'[]')
  render()
  document.getElementById('sendBtn').addEventListener('click', onSend)
  document.getElementById('groundBtn').addEventListener('click', onGround)
  document.getElementById('clearBtn').addEventListener('click', onClear)
  document.getElementById('downloadBtn').addEventListener('click', onDownload)
}

function save(){ localStorage.setItem('gohappily_history', JSON.stringify(window.historyData)) }

function render(){
  const conv = document.getElementById('conversation')
  conv.innerHTML = ''
  for(let i=window.historyData.length-1;i>=0;i--){
    const [who,msg] = window.historyData[i]
    const div = document.createElement('div')
    div.className = 'msg ' + (who==='You' ? 'you' : 'bot')
    div.innerHTML = `<strong>${who}:</strong> <div>${escapeHtml(msg)}</div>`
    conv.appendChild(div)
  }
}

function escapeHtml(s){ return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;') }

function onSend(){
  const userMsg = document.getElementById('userMsg').value.trim()
  const responseType = document.getElementById('responseType').value
  if(!userMsg){ alert('Please type a little about how you are feeling.'); return }
  window.historyData.push(['You', userMsg])
  const resp = makeResponse(userMsg, responseType)
  window.historyData.push(['GoHappily', resp])
  save(); render(); document.getElementById('userMsg').value=''
}

function onGround(){ const resp = groundingExercise(); window.historyData.push(['GoHappily', resp]); save(); render(); }
function onClear(){ if(confirm('Clear conversation?')){ window.historyData=[]; save(); render(); } }
function onDownload(){
  const txt = window.historyData.map(([s,t])=>`${s}: ${t}`).join('\n\n')
  const blob = new Blob([txt],{type:'text/plain'})
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href=url; a.download='gohappily_conversation.txt'; a.click(); URL.revokeObjectURL(url)
}

function groundingExercise(){
  const steps = [
    'Name 5 things you can see.',
    'Name 4 things you can touch.',
    'Name 3 things you can hear.',
    'Name 2 things you can smell.',
    'Name 1 thing you can taste (or imagine a taste).',
  ]
  return 'Try this 5-4-3-2-1 grounding: ' + steps.join(' ')
}

function cbtReframe(msg){
  return "Let's try a small reframe: what evidence supports this thought? What would you tell a friend in this situation? How might you test this belief?"
}

function motivate(msg){
  const lines = [
    'Small steps add up — one gentle step at a time.',
    'You are doing better than you think; progress is often quiet.',
    'Be kind to yourself today; you deserve patience and care.',
  ]
  if(msg && msg.toLowerCase().includes('tired')) lines.push("Rest is productive. It's okay to pause and recharge.")
  return lines[Math.floor(Math.random()*lines.length)]
}

function makeResponse(userMsg, responseType){
  if(responseType==='Support') return `I hear you: "${userMsg}". It's okay to feel that way.\n\n${motivate(userMsg)}`
  if(responseType==='Quote'){ const [q,src]=QUOTES[Math.floor(Math.random()*QUOTES.length)]; return `"${q}" — ${src}` }
  if(responseType==='Grounding') return groundingExercise()
  if(responseType==='Reframe') return cbtReframe(userMsg)
  if(responseType==='Practical Tip') return "Try a tiny, specific next step: what's one 5-minute action you can take now?"
  return "I'm here with you. Tell me more."
}

window.addEventListener('load', init)
