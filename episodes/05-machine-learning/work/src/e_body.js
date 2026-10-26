// 显示器（电脑）
function monitor(x,y,s,col=INK,alpha=1,face=''){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);
 X.fillStyle=SOFT;X.strokeStyle=col;X.lineWidth=5;X.beginPath();X.roundRect(-90,-70,180,130,14);X.fill();X.stroke();
 X.beginPath();X.moveTo(-26,60);X.lineTo(-36,92);X.lineTo(36,92);X.lineTo(26,60);X.stroke();
 if(face){X.fillStyle=col;X.font=`900 44px ${SANS}`;X.textAlign='center';X.textBaseline='middle';X.fillText(face,0,-4);}X.restore();}
const fmt=n=>Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,',');
function body(t){
 // 第一步
 const s1=env(t,S('L05')+0.9,S('L06'));if(s1.a>0)text('一张纸，只写一个概念',500,860+s1.dy,44,MUTE,SERIF,'center',700,s1.a);
 // 第二步：孩子 + 划掉术语
 const s2=env(t,S('L06')+0.2,S('L07')+0.1);
 if(s2.a>0){X.save();X.globalAlpha*=s2.a;X.translate(0,s2.dy);
  person(330,880,1,INK);tag('十二岁',330,1150,RED,true,32,1);
  const t0=at('L06','，');
  ['神经网络','梯度下降','损失函数'].forEach((wd,i)=>{const yy=760+i*130,e=eo(P(t,t0+i*0.25,t0+0.4+i*0.25));if(e>0){tag(wd,640,yy,MUTE,false,36,e);
   const sk=eo(P(t,at('L06','用')+0.1+i*0.25,at('L06','用')+0.35+i*0.25));if(sk>0)stroke([[545,yy+6],[735,yy-6]],sk,6,RED);}});
  X.restore();}
 label(t,S('L06')+0.2,S('L07')+0.1,[['不许用',INK],['术语',RED]]);
 // L07 以前：照规则做
 const r7=env(t,S('L07'),S('L08')+0.05);
 if(r7.a>0){X.save();X.globalAlpha*=r7.a;X.translate(0,r7.dy);
  label(t,S('L07'),S('L08')+0.05,[['以前的电脑：',INK],['照规则做',RED]]);
  const tr=at('L07','：');
  ['规则一：如果……就……','规则二：如果……就……','规则三：如果……就……'].forEach((r,i)=>{const e=eo(P(t,tr+i*0.35,tr+0.35+i*0.35));if(e<=0)return;
   tag(r,370,770+i*120,i===0?INK:MUTE,false,30,e);
   const a=eo(P(t,tr+0.2+i*0.35,tr+0.55+i*0.35));stroke([[560,770+i*120],[600,770+i*120]],a,5,RED);if(a>0.9)arrowHead(606,770+i*120,0,12,RED);});
  const m=spring(t-(tr+0.3));if(m>0){X.save();X.translate(710,890);X.scale(cl(m,0,1.1),cl(m,0,1.1));monitor(0,0,1,INK,cl(m*2),'照做');X.restore();}
  const n=eo(P(t,at('L07','，',2),at('L07','，',2)+0.4));mixed([['人写一条，',INK],['它做一条',RED]],500,1130,46,SERIF,900,n);
  X.restore();}
 // L08 猫是什么样子？规则写不出来
 const r8=env(t,S('L08'),S('L09')+0.05);
 if(r8.a>0){X.save();X.globalAlpha*=r8.a;X.translate(0,r8.dy);
  label(t,S('L08'),S('L09')+0.05,[['有些事，',INK],['规则写不出来',RED]]);
  const q=eo(P(t,at('L08','，',2),at('L08','，',2)+0.4));text('给猫写规则？',500,730,48,INK,SERIF,'center',900,q);
  const R=[['有尖耳朵','狐狸也有'],['有胡子','老鼠也有'],['四条腿','狗也有']],tq=at('L08','？')-0.2;
  R.forEach((r,i)=>{const e=eo(P(t,tq-0.9+i*0.35,tq-0.55+i*0.35));if(e<=0)return;const y=830+i*100;
   tag(r[0],330,y,INK,false,34,e);const b=eo(P(t,tq+0.1+i*0.25,tq+0.45+i*0.25));text('← '+r[1],520,y+12,34,MUTE,SANS,'left',700,b);
   if(b>0)stroke([[250,y+4],[410,y-4]],b,5,RED);});
  const no=spring(t-(at('L08','？')+0.3));if(no>0){X.save();X.translate(500,1150);X.scale(cl(no,0,1.15),cl(no,0,1.15));tag('说不清',0,0,RED,true,44,cl(no*2));X.restore();}
  X.restore();}
 // L09 不写规则，给例子
 const r9=env(t,S('L09'),S('L10')+0.05);
 if(r9.a>0){X.save();X.globalAlpha*=r9.a;X.translate(0,r9.dy);
  label(t,S('L09'),S('L10')+0.05,[['机器学习',RED],['换了个办法',INK]]);
  const a=eo(P(t,at('L09','：'),at('L09','：')+0.35));if(a>0){tag('写规则',500,800,MUTE,false,56,a);
   stroke([[380,812],[620,788]],P(t,at('L09','：')+0.4,at('L09','，')),8,RED);}
  const k=spring(t-at('L09','，'));
  if(k>0){stroke([[500,870],[500,930]],cl(k),5,RED);arrowHead(500,940,Math.PI/2,14,RED);
   X.save();X.translate(500,1030);X.scale(cl(k,0,1.12),cl(k,0,1.12));tag('给例子',0,0,RED,true,64,cl(k*2));X.restore();}
  X.restore();}
 // L10 一万张带标签的图
 const r10=env(t,S('L10'),S('L11')+0.05);
 if(r10.a>0){X.save();X.globalAlpha*=r10.a;X.translate(0,r10.dy);
  const G=['cat','dog','cat','cup','cat','ball','cat','dog','cat'],tg=S('L10')+0.15,tl=at('L10','：');
  G.forEach((k,i)=>{const r=Math.floor(i/3),c=i%3,e=spring(t-(tg+i*0.09));if(e<=0)return;
   const lb=t>=tl+i*0.12?(k==='cat'?'猫':'不是猫'):'';
   X.save();X.translate(270+c*230,720+r*185);X.scale(cl(e,0,1.1),cl(e,0,1.1));tile(0,0,150,k,lb,k==='cat',cl(e*2));X.restore();});
  const n=eo(P(t,at('L10','，'),at('L10','，')+0.6));
  if(n>0){X.save();X.globalAlpha*=n;X.fillStyle=RED;X.beginPath();X.roundRect(630,1060,240,74,37);X.fill();X.restore();
   text('× 一万张',750,1110,40,CARD,SANS,'center',900,n);}
  label(t,S('L10'),S('L11')+0.05,[['每张都',INK],['标好答案',RED]],618,44);
  X.restore();}
 // L11 猜 → 错 → 改一点点（循环）
 const r11=env(t,S('L11'),S('L12')+0.05);
 if(r11.a>0){X.save();X.globalAlpha*=r11.a;X.translate(0,r11.dy);
  label(t,S('L11'),S('L12')+0.05,[['猜，错了就',INK],['改一点点',RED]]);
  tile(290,830,190,'cat','',true,1);
  const c0=at('L11','。')-0.2,per=(E('L11')-c0)/3,ci=cl(Math.floor((t-c0)/per),0,2),ph=(t-c0-ci*per)/per;
  const guess=['猜：杯子','猜：狗','猜：猫'][ci],right=ci===2;
  if(t>=c0){bubble(650,760,330,96,1,SOFT,true);text(guess,650,776,42,INK,SANS,'center',700);
   const r=eo(P(ph,0.35,0.6));if(right){check(780,860,26,r);}else cross(780,860,24,r);
   // 旋钮：每错一次转一点
   const ang=-0.9+0.45*(ci+(right?0:eio(P(ph,0.6,0.95))));
   X.save();X.translate(650,1000);X.beginPath();X.arc(0,0,64,0,Math.PI*2);X.fillStyle=CARD;X.fill();X.lineWidth=5;X.strokeStyle=INK;X.stroke();
   for(let k=-4;k<=4;k++){const a=-Math.PI/2+k*0.3;X.beginPath();X.moveTo(Math.cos(a)*74,Math.sin(a)*74);X.lineTo(Math.cos(a)*86,Math.sin(a)*86);X.lineWidth=3;X.strokeStyle=MUTE;X.stroke();}
   X.rotate(ang);X.beginPath();X.moveTo(0,0);X.lineTo(0,-52);X.lineWidth=8;X.lineCap='round';X.strokeStyle=RED;X.stroke();X.restore();
   text('改一点点',650,1120,32,MUTE,SANS,'center',700,1);}
  X.restore();}
 // L12 几百万次 → 模型
 const r12=env(t,S('L12'),S('L13')+0.05);
 if(r12.a>0){X.save();X.globalAlpha*=r12.a;X.translate(0,r12.dy);
  const cnt=Math.pow(eio(P(t,S('L12')+0.1,at('L12','。'))),3)*3000000;
  text('改了',500,720,40,MUTE,SANS,'center',700,1);
  text(fmt(Math.max(1,cnt))+' 次',500,830,96,RED,SERIF,'center',900,1);
  text('（次数仅为示意）',500,880,26,MUTE,SANS,'center',500,eo(P(t,S('L12')+0.3,S('L12')+0.6)));
  const m=spring(t-at('L12','，',2));
  if(m>0){X.save();X.translate(500,1030);X.scale(cl(m,0,1.12),cl(m,0,1.12));X.globalAlpha*=cl(m*2);
   X.shadowColor=RED;X.shadowBlur=30*cl(m);X.fillStyle=RED;X.beginPath();X.roundRect(-150,-62,300,124,24);X.fill();X.shadowBlur=0;
   X.fillStyle=CARD;X.font=`900 64px ${SERIF}`;X.textAlign='center';X.textBaseline='middle';X.fillText('模型',0,4);X.restore();VIS.push('模型');
   text('＝ 练好的那个东西',500,1140,32,MUTE,SANS,'center',700,cl(m));}
  X.restore();}
 label(t,S('L12'),S('L13')+0.05,[['自己',INK],['摸出门道',RED]]);
 // 第三步：卡点
 const s13=env(t,S('L13'),S('L14'));
 if(s13.a>0){label(t,S('L13'),S('L14'),[['卡住的地方',INK]]);
  const k=spring(t-at('L13','：'));if(k>0){X.save();X.globalAlpha*=s13.a;X.translate(500,880);X.scale(k,k);
   X.beginPath();X.arc(0,0,195,0,Math.PI*2);X.lineWidth=6;X.setLineDash([16,12]);X.strokeStyle=RED;X.stroke();X.restore();
   text('学会了，',500,868,52,RED,SERIF,'center',900,s13.a*cl(k));text('就是真懂了？',500,944,52,RED,SERIF,'center',900,s13.a*cl(k));}}
 // L14 只是例子里的规律
 const r14=env(t,S('L14'),S('L15')+0.05);
 if(r14.a>0){X.save();X.globalAlpha*=r14.a;X.translate(0,r14.dy);
  label(t,S('L14'),S('L15')+0.05,[['其实',INK],['不是',RED]]);
  const a=eo(P(t,at('L14','。'),at('L14','。')+0.4));
  ['cat','cat','cat'].forEach((k,i)=>tile(300+i*200,800,150,k,'',false,a));
  const b=eo(P(t,at('L14','，')+0.1,at('L14','，')+0.5));
  mixed([['它学到的，只是',INK]],500,990,44,SERIF,900,b);mixed([['例子里的规律',RED]],500,1080,64,SERIF,900,b);
  X.restore();}
 // L15 沙发猫
 const r15=env(t,S('L15'),S('L16')+0.05);
 if(r15.a>0){X.save();X.globalAlpha*=r15.a;X.translate(0,r15.dy);
  label(t,S('L15'),S('L16')+0.05,[['猫，全在',INK],['沙发上',RED]]);
  const t1=at('L15','，'),t3=at('L15','，',3);
  [0,1,2].forEach(i=>{const e=spring(t-(S('L15')+0.3+i*0.2));if(e>0){X.save();X.translate(240+i*175,790);X.scale(cl(e,0,1.1),cl(e,0,1.1));tile(0,0,150,'cat','猫',true,cl(e*2),true);X.restore();}});
  // 空沙发 → 它说「猫！」
  const s=spring(t-(at('L15','，',2)+0.1));
  if(s>0){X.save();X.translate(500,1010);X.scale(cl(s,0,1.1),cl(s,0,1.1));tile(0,0,170,'none','',false,cl(s*2),true);X.restore();
   const say=eo(P(t,t3,t3+0.35));if(say>0){bubble(760,960,200,90,say,SOFT,true);text('猫！',760,976,46,INK,SANS,'center',900,say);}
   cross(760,960,40,P(t,E('L15')-0.4,E('L15')+0.1));
   text('沙发 ＝ 猫的一部分？',500,1150,36,RED,SANS,'center',700,eo(P(t,t3+0.4,t3+0.8)));}
  X.restore();}
 // L16 例子歪了，就学歪了
 const r16=env(t,S('L16'),S('L17')+0.05);
 if(r16.a>0){X.save();X.globalAlpha*=r16.a;X.translate(0,r16.dy);
  const a=eo(P(t,S('L16')+0.1,S('L16')+0.5)),b=eo(P(t,at('L16','，')+0.1,at('L16','，')+0.5));
  X.save();X.translate(330,800);X.rotate(-0.12*a);tag('例子歪了',0,0,INK,false,44,a);X.restore();
  stroke([[450,800],[530,800]],b,5,RED);if(b>0.9)arrowHead(540,800,0,13,RED);
  X.save();X.translate(670,800);X.rotate(0.12*b);tag('学歪了',0,0,RED,true,44,b);X.restore();
  const c=eo(P(t,at('L16','。')+0.1,at('L16','。')+0.5)),d=eo(P(t,at('L16','，',2),at('L16','，',2)+0.4));
  text('更重要的是',500,950,36,MUTE,SANS,'center',700,c);
  if(c>0){X.save();X.translate(330,1060);X.scale(lerp(0.8,1.15,d),lerp(0.8,1.15,d));tag('喂它什么',0,0,RED,true,48,c);X.restore();}
  text('＞',500,1076,56,INK,SERIF,'center',900,d);tag('它多聪明',680,1060,MUTE,false,40,d);
  X.restore();}
 label(t,S('L16'),S('L17')+0.05,[['喂什么，',RED],['学什么',INK]]);
 // 第四步：一句话
 const os=env(t,at('L17','：')-0.1,S('L18')+0.1,0.3,0.3);
 label(t,S('L17'),at('L17','：'),[['简化成',INK],['一句话',RED]]);
 if(os.a>0){const s=lerp(1.2,1,eo(P(t,at('L17','：'),at('L17','：')+0.3)));X.save();X.translate(500,800);X.scale(s,s);X.translate(-500,-800);
  text('机器学习',500,760+os.dy,128,RED,SERIF,'center',900,os.a);
  mixed([['就是让电脑',INK]],500,890,60,SERIF,900,os.a*eo(P(t,at('L17','，',2)-0.2,at('L17','，',2)+0.3)),os.dy);
  mixed([['从',INK],['例子',RED],['里',INK]],500,990,60,SERIF,900,os.a*eo(P(t,at('L17','从')-0.1,at('L17','从')+0.3)),os.dy);
  mixed([['自己找规律',RED]],500,1105,80,SERIF,900,os.a*eo(P(t,at('L17','里')+0.05,at('L17','里')+0.45)),os.dy);X.restore();}
 // L18 树枝：根 → B → B7 → B7.2（亮），旁边 B7.1 兄弟，往上一层虚线
 const m=env(t,S('L18'),S('L19')+0.1);
 if(m.a>0){X.save();X.globalAlpha*=m.a;
  text('这张卡挂在树上的位置',500,600,40,MUTE,SERIF,'center',700);
  const N=[['01 三观（根）',500,1150],['B 世界怎么运转',500,1040],['B7 科技与变化',500,930],['B7.1 Token',300,820],['B7.2 机器学习',650,820]];
  const t0=S('L18')+0.2,tb=at('L18','：');
  for(let i=0;i<5;i++){const ti=t0+Math.min(i,3)*0.35+(i===4?0.25:0),e=eo(P(t,ti,ti+0.4));if(e<=0)continue;
   const p=i===4?2:i-1;if(i>0){stroke([[N[p][1],N[p][2]-30],[N[i][1],N[i][2]+30]],e,5,i===4?RED:(i===3?MUTE:INK));}
   tag(N[i][0],N[i][1],N[i][2],i===4?RED:(i===3?MUTE:INK),i===4,i===4?36:30,e);}
  const nx=eo(P(t,tb,tb+0.5));if(nx>0){X.save();X.globalAlpha*=nx;X.setLineDash([10,10]);X.strokeStyle=RED;X.lineWidth=4;X.beginPath();X.moveTo(650,790);X.lineTo(650,735);X.stroke();X.restore();
   const lbl='模型怎么一点点改对？';X.save();X.globalAlpha*=nx;X.font=`700 30px ${SANS}`;const w=X.measureText(lbl).width+40;X.beginPath();X.roundRect(650-w/2,684,w,52,26);X.setLineDash([10,8]);X.lineWidth=3;X.strokeStyle=RED;X.stroke();
   X.fillStyle=RED;X.textAlign='center';X.textBaseline='middle';X.fillText(lbl,650,711);X.restore();VIS.push(lbl);
   text('下一层',650,668,26,MUTE,SANS,'center',500,nx);}
  X.restore();}
 // L19–L20 今晚想一想
 const f=env(t,S('L19'),A.end+0.1);
 if(f.a>0){X.save();X.globalAlpha*=f.a;X.translate(0,f.dy);
  mixed([['今晚',INK],['想一想',RED]],500,650,56,SERIF,900,1);
  const q=eo(P(t,at('L19','：'),at('L19','：')+0.4));mixed([['你哪个本事，是',INK],['看例子',RED],['学会的？',INK]],500,750,44,SERIF,900,q);
  ['骑自行车','说母语','看人脸色'].forEach((s,i)=>{const k=spring(t-(at('L19','，')+0.1+i*0.3));if(k>0){X.save();X.translate(260+i*240,870);X.scale(cl(k,0,1.1),cl(k,0,1.1));tag(s,0,0,i===1?RED:INK,false,36,cl(k*2));X.restore();}});
  const nb=eo(P(t,at('L19','，',2),at('L19','，',2)+0.4));text('而不是背规则背会的',500,990,40,MUTE,SERIF,'center',700,nb);
  if(nb>0)stroke([[330,978],[670,978]],eo(P(t,at('L19','，',2)+0.4,E('L19'))),4,MUTE);
  const cm=spring(t-S('L20'));if(cm>0){X.save();X.translate(500,1120);X.scale(cl(cm),cl(cm));X.beginPath();X.roundRect(-190,-40,380,80,40);X.fillStyle=SOFT;X.fill();
   X.beginPath();X.moveTo(-120,36);X.lineTo(-150,64);X.lineTo(-90,38);X.fill();X.restore();text('评论区告诉我',500,1132,36,INK,SANS,'center',700,cl(cm*2));}
  X.restore();}
}
// ================= 片尾 =================
function endcard(t){
 const e=(d)=>eo(P(t,A.end+0.5+d,A.end+1.0+d));
 if(t<A.end+0.5)return;
 const a=e(0),b=e(0.25),c=e(0.6),d=e(0.9);
 const seed=(window.META&&window.META.music_seed)?' · 种子 '+window.META.music_seed:'';
 text('费曼学习法卡片',500,600+(1-a)*30,92,INK,SERIF,'center',900,a);
 text('05 · 机器学习',500,700+(1-b)*30,60,RED,SERIF,'center',700,b);
 text('B7.2 · 上级 B7 科技与变化',500,752+(1-b)*30,28,MUTE,SANS,'center',500,b);
 if(b>0){X.save();X.globalAlpha=b;X.fillStyle=SOFT;X.fillRect(300,785,400,3);X.restore();}
 text('出处：作者自我认知（Shaomanman）',500,870+(1-c)*24,38,INK,SANS,'center',500,c);
 text('许可：CC BY 4.0（署名 4.0 国际）',500,935+(1-c)*24,38,INK,SANS,'center',500,c);
 text('creativecommons.org/licenses/by/4.0',500,992+(1-c)*24,28,MUTE,SANS,'center',500,c);
 text('配乐：ACE-Step 1.5 本地生成（MIT）'+seed,500,1050+(1-c)*24,26,MUTE,SANS,'center',500,c);
 text('配音：Qwen3-TTS 本地生成（参考 ElevenLabs Brian 音色）',500,1090+(1-c)*24,26,MUTE,SANS,'center',500,c);
 text('下一张卡片见',500,1190+(1-d)*24,58,RED,SERIF,'center',900,d);
}
