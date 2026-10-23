// speechSynthesis helpers shared by the app and the audio test page.
// iOS only lets a page speak if speech was first started directly inside a tap handler (no await
// before it), so prime() must be called synchronously from user gestures.

const synth = window.speechSynthesis;
let voices = [];
function load() { try { voices = synth.getVoices() || []; } catch (e) { voices = []; } return voices; }
load();
try { synth.addEventListener('voiceschanged', load); } catch (e) {}

// English voices, best first: Apple Premium, then Enhanced, then the rest; US/GB before other accents.
export function englishVoices() {
  load();
  const score = v => (/premium/i.test(v.name) ? 0 : /enhanced/i.test(v.name) ? 10 : 20)
    + (/en[-_]US/i.test(v.lang) ? 0 : /en[-_]GB/i.test(v.lang) ? 1 : 3)
    + (/compact|eloquence|grandma|grandpa|rocko|reed|sandy|shelley|flo|eddy|bahh|bells|boing|bubbles|cellos|wobble|jester|organ|superstar|trinoids|whisper|zarvox|albert|bad news|good news|fred|junior|ralph|kathy/i.test(v.name) ? 50 : 0);
  return voices.filter(v => /^en/i.test(v.lang)).sort((a, b) => score(a) - score(b) || a.name.localeCompare(b.name));
}
export function pickVoice(uri) {
  const list = englishVoices();
  return list.find(v => v.voiceURI === uri) || list[0] || null;
}
export const isGood = v => !!v && /premium|enhanced/i.test(v.name);

// Call synchronously at the top of every tap handler that might lead to speech.
export function prime() {
  try { if (synth.speaking || synth.pending) return; const u = new SpeechSynthesisUtterance(' '); u.volume = 0; synth.speak(u); } catch (e) {}
}

// Split into sentence groups of ~200 characters; iOS can stall on very long single utterances.
export function chunks(text) {
  const sents = String(text).replace(/\s+/g, ' ').match(/[^.!?]+[.!?]+["')\]]*\s*|[^.!?]+$/g) || [text];
  const out = []; let cur = '';
  for (const s of sents) { if ((cur + s).length > 220 && cur) { out.push(cur.trim()); cur = ''; } cur += s; }
  if (cur.trim()) out.push(cur.trim());
  return out;
}

// Speak text as a queue of utterances. Returns a handle; onend fires once, after the last chunk.
export function speak(text, { voiceURI, rate = 1, volume = 1, onstart, onend } = {}) {
  const voice = pickVoice(voiceURI);
  const parts = chunks(text);
  let done = false, started = false;
  const finish = () => { if (!done) { done = true; onend && onend(); } };
  try { synth.cancel(); } catch (e) {}
  parts.forEach((p, i) => {
    const u = new SpeechSynthesisUtterance(p);
    if (voice) { u.voice = voice; u.lang = voice.lang; } else u.lang = 'en-US';
    u.rate = rate; u.volume = volume;
    u.onstart = () => { if (!started) { started = true; onstart && onstart(); } };
    if (i === parts.length - 1) { u.onend = finish; }
    u.onerror = e => { if (e.error !== 'interrupted' && e.error !== 'canceled') finish(); };
    synth.speak(u);
  });
  return { cancel() { done = true; try { synth.cancel(); } catch (e) {} } };
}

// Experimental "ducker": while a recorded clip plays in a mixable audio session, keep a silent
// (volume 0) speech utterance running, hoping iOS ducks other audio for speech as it does in mode E.
let duckOn = false;
export function startDuck(text) {
  duckOn = true;
  const loop = () => {
    if (!duckOn) return;
    const u = new SpeechSynthesisUtterance(chunks(text).slice(0, 3).join(' ') || 'pause');
    u.volume = 0; u.rate = 0.7;
    u.onend = () => setTimeout(loop, 0);
    try { synth.speak(u); } catch (e) {}
  };
  try { synth.cancel(); } catch (e) {}
  loop();
}
export function stopDuck() { duckOn = false; try { synth.cancel(); } catch (e) {} }
export const speaking = () => synth.speaking;
export const pause = () => synth.pause();
export const resume = () => synth.resume();
export const paused = () => synth.paused;
