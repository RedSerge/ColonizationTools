var c : array [0..3] of byte; b : byte; code : integer;
var f : file of byte; fn : string;
begin
fn:='01111';
c[0]:=1;c[1]:=1;c[2]:=1;c[3]:=1;
if paramcount>0 then fn:=paramstr(1);
for b:=0 to 3 do val(fn[b+2],c[b],code);
fn:='colony0'+fn[1]+'.sav';
assign(f,fn);
reset(f);
seek(f,207);
write(f,c[0]);
seek(f,259);
write(f,c[1]);
seek(f,311);
write(f,c[2]);
seek(f,363);
write(f,c[3]);
close(f);
end.