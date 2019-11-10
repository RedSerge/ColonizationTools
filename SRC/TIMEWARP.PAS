type city = array [1..202] of byte;
type sav = record
  cities : array [1..255] of city;
  count : byte;
  pos : longint;
end;
type bytefile = file of byte;
type bits=array [0..7] of byte;
var bs:bits;

procedure bit(var b:byte;var somebits:bits);
var n:byte;
begin
  for n:=0 to 7 do somebits[n]:=(b shr (7-n)) and 1;
end;

procedure unbit(var b:byte;var somebits:bits);
var n:byte;base:byte;
begin
  base:=1;b:=0;
  for n:=7 downto 0 do begin
    if somebits[n]<>0 then b:=b+base;
    base:=base*2;
  end;
end;

procedure read_sav(var f : bytefile; var save : sav);
var i,j : byte;
begin
  reset(f);
  seek(f,46);
  read(f,save.count);
  seek(f,390);
  for i:=1 to save.count do for j:=1 to 202 do read(f,save.cities[i][j]);
  save.pos:=filepos(f);
  close(f);
end;

function pass(var c1 : city; var c2 : city) : boolean;
begin
  pass:=(c1[1]=c2[1]) and (c1[2]=c2[2]) and (c1[27]=c2[27]);
end;

procedure chbit(var f : bytefile; var b : byte; var p : byte);
begin
  if p=29 then begin
    bit(b,bs);
    bs[7]:=0;
    unbit(b,bs);
  end;
  write(f,b);
end;

var fn : string; f_base : string; f_future : string; f_warp : string;
var f1,f2 : bytefile; save : array [1..2] of ^sav; i,j,k : byte;
var p : longint; passed : boolean;

begin
  fn:='012';
  if paramcount>0 then fn:=paramstr(1);
  f_base:=  'colony0'+fn[1]+'.sav';
  f_future:='colony0'+fn[2]+'.sav';
  f_warp:=  'colony0'+fn[3]+'.sav';
  getmem(save[1],sizeof(sav));
  getmem(save[2],sizeof(sav));

  assign(f1,f_future);
  read_sav(f1,save[2]^);
  assign(f1,f_base);
  read_sav(f1,save[1]^);

  assign(f2,f_warp);
  reset(f1);
  rewrite(f2);
  for p:=1 to 390 do begin
    read(f1,i);
    write(f2,i);
  end;
  for j:=1 to save[1]^.count do begin
    for k:=1 to 27 do write(f2,save[1]^.cities[j][k]);
    passed:=false;
    for i:=1 to save[2]^.count do begin
      passed:=pass(save[1]^.cities[j],save[2]^.cities[i]);
      if passed then begin
        for k:=28 to 202 do chbit(f2,save[2]^.cities[i][k],k);
        break;
      end;
    end;
    if not passed then for k:=28 to 202 do chbit(f2,save[1]^.cities[j][k],k);
  end;
  seek(f1,390+202*j);
  while not eof(f1) do begin
    read(f1,i);
    write(f2,i);
  end;
  close(f2);

  freemem(save[2],sizeof(sav));
  freemem(save[1],sizeof(sav));
end.