import {build} from 'esbuild';
await build({entryPoints:['frontend/famiglie.js'],bundle:true,minify:true,format:'iife',target:['es2020'],outfile:'../dist/famiglie.js',legalComments:'none'});
