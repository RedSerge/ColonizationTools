procedure store(var f:text);
var t:array [0..3] of integer;
var e:array [1..3] of integer;
var i,j,k,p,u:integer;
var b:boolean;
begin
for j:=0 to 10 do t[0]:=random(27);
for i:=0 to 3 do while true do begin
  t[i]:=random(27);
  b:=true;
  for j:=0 to i-1 do if t[j]=t[i] then begin
    b:=false; break;
  end;
  if b then break;
end;
for p:=0 to 3 do begin
  j:=t[p];
  for k:=1 to 3 do begin
    i:=j mod 3;
    e[k]:=i-1;
    j:=j div 3;
  end;
  write(f,chr(13),chr(10));
  if t[p]=13 then write(f,'Faceless') else begin
  b:=false;
  case e[1] of
    -1:begin write(f,'Kind');b:=true; end;
    1:begin write(f,'Cruel');b:=true; end;
  end;
  case e[2] of
    -1:begin if b then write(f, ' ');write(f,'Moderate');b:=true; end;
    1:begin if b then write(f, ' ');write(f,'Greedy');b:=true; end;
  end;
  case e[3] of
    -1:begin if b then write(f, ' ');write(f,'Militant'); end;
    1:begin if b then write(f, ' ');write(f,'Cultured'); end;
  end;
  end;
  for i:=1 to 3 do write(f,',',e[i]);
end;
end;

var t,d:text;c:char;s:string;s_len,pos:integer;
begin
randomize;
pos:=0;
s:='@LEADERNAME';
s_len:=length(s);
assign(d,'names.txt');
assign(t,'names.old');
rewrite(d);
reset(t);
while not eof(t) do begin
  read(t,c);
  if pos>s_len then pos:=0;
  if ord(c)=13 then begin
    if pos=s_len then begin
       store(d);
    end;
    pos:=0;
  end;
  if c=s[pos+1] then inc(pos);
  write(d,c);
end;
close(d);
close(t);
end.