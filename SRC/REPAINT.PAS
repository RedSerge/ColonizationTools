var c : array [0..3] of byte; cnt, b, i : byte; code : integer;
var f : file of byte; fn : string; p : longint;
begin
fn:='01230';
c[0]:=1;c[1]:=2;c[2]:=3;c[3]:=0;
if paramcount>0 then fn:=paramstr(1);
for b:=0 to 3 do val(fn[b+2],c[b],code);
fn:='colony0'+fn[1]+'.sav';
assign(f,fn);
reset(f);
seek(f,46);
read(f,cnt);
if cnt=0 then exit;
dec(cnt);
for i:=0 to cnt do begin
  p:=390+202*i+26;
  seek(f,p);
  read(f,b);
  b:=c[b];
  seek(f,p);
  write(f,b);
end;
end.