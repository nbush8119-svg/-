// ================= 音效事件 =================
(function(){ev(S('L01')+0.1,'pop');ev(at('L01','？')+0.1,'strike');ev(at('L01','？')+0.35,'strike');
 [0,1,2].forEach(i=>ev(S('L02')+0.3+i*0.45,'pop'));ev(at('L02','：'),'stamp');ev(at('L02','。')+0.1,'whoosh');ev(at('L02','，')+0.3,'chime');
 ev(S('L03')+0.15,'stamp');
 ev(S('L04')-0.1,'whoosh');[0,0.35,0.7,1.05].forEach(d=>ev(at('L04','，')+0.1+d,'tick'));
 ev(S('L05')-0.15,'whoosh');ev(at('L05','：'),'pen');ev(S('L06'),'tick');[0.1,0.35,0.6].forEach(d=>ev(at('L06','用')+d,'strike'));
 [0,1,2].forEach(i=>ev(at('L07','：')+i*0.35,'tick'));ev(at('L07','：')+0.3,'pop');
 [0,1,2].forEach(i=>ev(at('L08','？')+0.1+i*0.25,'strike'));ev(at('L08','？')+0.3,'stamp');
 ev(at('L09','：')+0.4,'strike');ev(at('L09','，'),'pop');
 for(let i=0;i<9;i++)ev(S('L10')+0.15+i*0.09,'tick');ev(at('L10','，'),'whoosh');
 {const c0=at('L11','。')-0.2,per=(E('L11')-c0)/3;for(let i=0;i<3;i++){ev(c0+i*per+0.02,'pop');ev(c0+i*per+per*0.4,i<2?'strike':'chime');}}
 ev(S('L12')+0.1,'whoosh');ev(at('L12','，',2),'stamp');
 ev(S('L13'),'tick');ev(at('L13','：'),'pop');ev(at('L14','。'),'whoosh');
 [0,1,2].forEach(i=>ev(S('L15')+0.3+i*0.2,'pop'));ev(at('L15','，',2)+0.1,'drop');ev(at('L15','，',3),'pop');ev(E('L15')-0.4,'strike');
 ev(S('L16')+0.1,'drop');ev(at('L16','，')+0.1,'drop');ev(at('L16','，',2),'stamp');
 ev(S('L17'),'tick');ev(at('L17','：'),'stamp');ev(S('L18')+0.2,'whoosh');ev(at('L18','：'),'pen');
 ev(S('L19'),'whoosh');[0,1,2].forEach(i=>ev(at('L19','，')+0.1+i*0.3,'pop'));ev(S('L20'),'pop');ev(A.end,'whoosh');ev(A.end+1.5,'chime');})();
