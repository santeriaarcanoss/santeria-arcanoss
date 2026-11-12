// Saca los textos del horóscopo directamente de la página (public/index.html),
// así las placas dicen siempre lo mismo que la web.
// Uso: TZ=America/Buenos_Aires node datos.mjs ../../public/index.html 2026-11-23 2026-11-26
import fs from "node:fs";
import vm from "node:vm";

const [, , htmlPath, ...fechas] = process.argv;
const html = fs.readFileSync(htmlPath, "utf8");
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).sort((a, b) => b.length - a.length)[0];

// DOM falso: absorbe cualquier acceso para que el script de la página corra sin navegador.
const fake = new Proxy(function () {}, {
  get(t, p) {
    if (p === Symbol.toPrimitive) return () => "";
    if (p === Symbol.iterator) return function* () {};
    if (p === "length") return 0;
    if (p === "then") return undefined;
    return fake;
  },
  apply: () => fake, construct: () => fake, set: () => true,
});
const ctx = {
  document: fake, navigator: { userAgent: "" }, location: { href: "", hash: "", search: "", pathname: "/" },
  localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
  IntersectionObserver: class { observe() {} unobserve() {} disconnect() {} },
  matchMedia: () => ({ matches: false, addEventListener() {}, addListener() {} }),
  setTimeout: () => 0, clearTimeout() {}, setInterval: () => 0, clearInterval() {}, requestAnimationFrame: () => 0,
  addEventListener() {}, removeEventListener() {}, fetch: () => new Promise(() => {}), Image: class {},
  URL, URLSearchParams, console, scrollTo() {}, innerWidth: 400, innerHeight: 800,
};
ctx.window = ctx; ctx.self = ctx;
vm.createContext(ctx);
vm.runInContext(code, ctx, { timeout: 10000 });

const extraer = (fechas) => fechas.map(f => {
  const [y, m, d] = f.split("-").map(Number);
  hoyLocal = () => new Date(y, m - 1, d, 12, 0, 0);
  const signos = ZS.map((z, i) => {
    const h = horoscopo(i);
    return { nombre: z[0], glifo: z[1], fechas: z[2], lead: h.lead, tono: h.tono, energia: h.en, etiqueta: h.lab,
             plan: h.plan, tip: h.tip, color: h.color, luna: h.moon };
  });
  return { fecha: f, luna: signos[0].luna, tip: signos[0].tip, color: signos[0].color, signos };
});
const out = vm.runInContext(`(${extraer.toString()})(${JSON.stringify(fechas)})`, ctx);
process.stdout.write(JSON.stringify(out, null, 1));
