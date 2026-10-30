// Generate dist/custom-elements.json and dist/types/*.d.ts from
// packages/elements/api.mjs. Called by packages/ui/build.mjs.
import fs from 'node:fs/promises';
import path from 'node:path';
import { ELEMENTS, EXTRA_TYPES } from '../../elements/api.mjs';

const camel = (s) => s.replace(/-(\w)/g, (_, c) => c.toUpperCase());
const pascal = (s) => camel(s)[0].toUpperCase() + camel(s).slice(1);
const doc = (text, indent = '  ') => `${indent}/** ${text} */\n`;

// ---- Custom Elements Manifest (schema 2.1.0)
function manifest(version) {
  return {
    schemaVersion: '2.1.0',
    readme: '',
    modules: ELEMENTS.map((el) => ({
      kind: 'javascript-module',
      path: `dist/${el.module}`,
      declarations: [{
        kind: 'class',
        name: el.className,
        tagName: el.tag,
        customElement: true,
        description: el.description,
        attributes: [
          ...(el.attributes || []).map((a) => ({ name: a.name, type: { text: a.type }, description: a.description })),
          ...el.properties.filter((p) => p.attribute).map((p) => ({ name: p.attribute, fieldName: p.name, type: { text: p.type }, description: p.description })),
        ],
        members: [
          ...el.properties.map((p) => ({ kind: 'field', name: p.name, type: { text: p.type }, description: p.description, ...(p.readonly && { readonly: true }) })),
          ...(el.methods || []).map((m) => ({ kind: 'method', name: m.name, description: m.description, type: { text: m.signature } })),
        ],
        events: el.events.map((e) => ({ name: e.name, type: { text: `CustomEvent<${e.detail}>` }, description: e.description })),
      }],
      exports: [{ kind: 'custom-element-definition', name: el.tag, declaration: { name: el.className, module: `dist/${el.module}` } }],
    })),
    package: { name: '@auvyx/ui', version },
  };
}

// ---- DOM types: element interfaces, event maps, HTMLElementTagNameMap
function domTypes() {
  const out = [`// Generated from packages/elements/api.mjs by packages/ui/tools/types.mjs. Do not edit.\n`, EXTRA_TYPES, ''];
  for (const el of ELEMENTS) {
    const map = `${el.className.replace(/Element$/, '')}EventMap`;
    out.push(`/** <${el.tag}>: ${el.description} */`);
    // Our events replace the DOM's of the same name (toggle is a ToggleEvent, resize a UIEvent there).
    out.push(`export interface ${map} extends Omit<HTMLElementEventMap, ${el.events.map((e) => JSON.stringify(e.name)).join(' | ') || 'never'}> {`);
    for (const e of el.events) out.push(doc(e.description) + `  ${JSON.stringify(e.name)}: CustomEvent<${e.detail}>;`);
    out.push('}');
    out.push(`export interface ${el.className} extends HTMLElement {`);
    for (const p of el.properties) out.push(doc(p.description) + `  ${p.readonly ? 'readonly ' : ''}${p.name}: ${p.type};`);
    for (const m of el.methods || []) out.push(doc(m.description) + `  ${m.name}${m.signature.replace(/ =>/, ':')};`);
    out.push(`  addEventListener<K extends keyof ${map}>(type: K, listener: (this: ${el.className}, ev: ${map}[K]) => any, options?: boolean | AddEventListenerOptions): void;`);
    out.push(`  addEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | AddEventListenerOptions): void;`);
    out.push(`  removeEventListener<K extends keyof ${map}>(type: K, listener: (this: ${el.className}, ev: ${map}[K]) => any, options?: boolean | EventListenerOptions): void;`);
    out.push(`  removeEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | EventListenerOptions): void;`);
    out.push('}', '');
  }
  out.push('declare global {', '  interface HTMLElementTagNameMap {');
  for (const el of ELEMENTS) out.push(`    ${JSON.stringify(el.tag)}: ${el.className};`);
  out.push('  }', '}', '');
  return out.join('\n');
}

// Writable properties a framework may set (attributes-only ones are strings).
const inputProps = (el) => [
  ...el.properties.filter((p) => !p.readonly && p.name !== 'renderDay').map((p) => ({ name: p.name, type: p.name === 'value' && p.type.includes('null') ? p.type.replace(' | null', '') : p.type, description: p.description })),
  ...(el.attributes || []).map((a) => ({ name: a.name, type: a.type === 'boolean' ? 'boolean' : a.type, description: a.description })),
];

// ---- React 19 JSX
// React maps onChange / onInput to the custom element's events and passes a
// SyntheticEvent; other names are passed through as written and receive the
// native event. onToggle and onSelect are React's own synthetic events and
// never fire for custom elements, so they are typed `never` with a pointer to
// the lowercase form.
function reactTypes() {
  const out = [
    `// Generated from packages/elements/api.mjs by packages/ui/tools/types.mjs. Do not edit.`,
    `// React 19 JSX types for <auvyx-*> elements: add  import type {} from "@auvyx/ui/types/react";  once.`,
    `import type { HTMLAttributes, Ref, ReactNode, SyntheticEvent } from 'react';`,
    `import type { ${ELEMENTS.map((e) => e.className).join(', ')} } from './elements';`,
    '',
    `type AuvyxBase<E> = Omit<HTMLAttributes<E>, 'onChange' | 'onInput' | 'onToggle' | 'onSelect'> & {`,
    `  ref?: Ref<E>;`,
    `  class?: string;`,
    `  children?: ReactNode;`,
    `  /** @deprecated React's onToggle never fires for custom elements. Use the lowercase \`ontoggle\`. */`,
    `  onToggle?: never;`,
    `  /** @deprecated React's onSelect never fires for custom elements. Use the lowercase \`onselect\`. */`,
    `  onSelect?: never;`,
    `};`,
    '',
  ];
  const synthetic = { change: 'onChange', input: 'onInput' };
  for (const el of ELEMENTS) {
    out.push(`export type ${el.className.replace(/Element$/, 'Props')} = AuvyxBase<${el.className}> & {`);
    for (const p of inputProps(el)) out.push(doc(p.description) + `  ${JSON.stringify(p.name)}?: ${p.type};`);
    for (const e of el.events) {
      const prop = synthetic[e.name];
      if (prop) out.push(doc(`${e.description}. Read event.currentTarget.value.`) + `  ${prop}?: (event: SyntheticEvent<${el.className}, CustomEvent<${e.detail}>>) => void;`);
      else out.push(doc(`${e.description}. Receives the native event.`) + `  ${JSON.stringify('on' + e.name)}?: (event: CustomEvent<${e.detail}> & { currentTarget: ${el.className} }) => void;`);
    }
    out.push('};', '');
  }
  out.push(`declare module 'react' {`, '  namespace JSX {', '    interface IntrinsicElements {');
  for (const el of ELEMENTS) out.push(`      ${JSON.stringify(el.tag)}: ${el.className.replace(/Element$/, 'Props')};`);
  out.push('    }', '  }', '}', '');
  return out.join('\n');
}

// ---- Vue 3 templates (Volar / vue-tsc read GlobalComponents)
function vueTypes() {
  const out = [
    `// Generated from packages/elements/api.mjs by packages/ui/tools/types.mjs. Do not edit.`,
    `// Vue 3 template types for <auvyx-*> elements: add  import type {} from "@auvyx/ui/types/vue";  once,`,
    `// and set app.config.compilerOptions.isCustomElement = (tag) => tag.startsWith('auvyx-').`,
    `import type { DefineComponent } from 'vue';`,
    `import type { ${ELEMENTS.map((e) => e.className).join(', ')} } from './elements';`,
    '',
  ];
  for (const el of ELEMENTS) {
    out.push(`type ${el.className.replace(/Element$/, 'VueProps')} = {`);
    for (const p of inputProps(el)) out.push(doc(p.description) + `  ${JSON.stringify(p.name)}?: ${p.type};`);
    for (const e of el.events) out.push(doc(e.description) + `  ${JSON.stringify('on' + pascal(e.name))}?: (event: CustomEvent<${e.detail}> & { target: ${el.className} }) => void;`);
    out.push('};');
  }
  out.push('', `declare module 'vue' {`, '  interface GlobalComponents {');
  for (const el of ELEMENTS) out.push(`    ${JSON.stringify(el.tag)}: DefineComponent<${el.className.replace(/Element$/, 'VueProps')}>;`);
  out.push('  }', '}', '');
  return out.join('\n');
}

export async function writeTypes(dist, version) {
  await fs.mkdir(path.join(dist, 'types'), { recursive: true });
  await fs.writeFile(path.join(dist, 'custom-elements.json'), JSON.stringify(manifest(version), null, 2) + '\n');
  await fs.writeFile(path.join(dist, 'types/elements.d.ts'), domTypes());
  await fs.writeFile(path.join(dist, 'types/react.d.ts'), reactTypes());
  await fs.writeFile(path.join(dist, 'types/vue.d.ts'), vueTypes());
}
