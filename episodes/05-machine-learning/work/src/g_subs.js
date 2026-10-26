// ================= 字幕（1300–1480px，x 60–920） =================
function subs(t){
 for(const c of CUES){if(t<c[0]||t>=c[1])continue;
  const lines=c[2].split('\n');const e=eo(P(t,c[0],c[0]+0.15));
  let size=50;X.font=`700 ${size}px ${SANS}`;const mw=Math.max(...lines.map(l=>X.measureText(l).width));if(mw>840)size=Math.floor(50*840/mw);
  const lh=lines.length>2?68:74,base=lines.length===1?1410:(lines.length===2?1374:1342);
  lines.forEach((ln,i)=>{const y=base+i*lh+(1-e)*8;
   const segs=[];let s=ln;while(s.length){let hit=null,idx=1e9;for(const k of KEY){const j=s.indexOf(k);if(j>=0&&j<idx){idx=j;hit=k;}}
    if(!hit){segs.push([s,INK]);break;}if(idx>0)segs.push([s.slice(0,idx),INK]);segs.push([hit,RED]);s=s.slice(idx+hit.length);}
   X.save();X.globalAlpha=e;X.font=`700 ${size}px ${SANS}`;X.textBaseline='alphabetic';
   const W=segs.reduce((q,g)=>q+X.measureText(g[0]).width,0);let x=490-W/2;
   for(const g of segs){X.lineWidth=10;X.strokeStyle=PAPER;X.lineJoin='round';X.strokeText(g[0],x,y);X.fillStyle=g[1];X.fillText(g[0],x,y);x+=X.measureText(g[0]).width;}
   X.restore();});
  VIS.push('SUB:'+c[2]);}
}
