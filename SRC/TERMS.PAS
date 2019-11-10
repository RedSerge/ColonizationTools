function bit(var b:byte;n:byte):byte;
begin
  bit:=(b shr (7-n)) and 1;
end;

var fi:file of integer;y:integer;
var f:file of byte;c,d,e:byte;b:array [0..3] of boolean;
var confirm,fn:string;fz:array [0..4] of integer;
const flash:byte=1;

procedure unfreeze(tory : boolean);
var c,d:byte;
begin
  for d:=0 to 3 do begin
    seek(f,fz[d]);
    read(f,c);
    if c=2 then begin
      seek(f,fz[d]);
      write(f,flash);
    end;
    if tory and (c=0) then begin
      seek(f,100);
      write(f,d);
      seek(f,101);
      c:=0;
      write(f,c);
    end;
  end;
end;

begin
  fn:='0';
  fz[0]:=207;
  fz[1]:=259;
  fz[2]:=311;
  fz[3]:=363;
  if paramcount>0 then fn:=paramstr(1);
  fn:='colony0'+fn[1]+'.sav';
  assign(fi,fn);
  assign(f,fn);
  reset(f);
  seek(f,98);
  read(f,c);
  if c=255 then begin
    seek(f,98);
    c:=10;
    write(f,c);
    c:=0;
    write(f,c);
    writeln('War of Succession has been suspended.');
  end else if c=10 then begin
    close(f);
    reset(fi);
    seek(fi,13);
    read(fi,y);
    close(fi);
    reset(f);
    if y<1600 then writeln('The time has not come yet...') else begin
      seek(f,46);
      read(f,c);
      for d:=1 to 3 do b[d]:=false;
      for d:=1 to c do begin
        seek(f,416+202*(d-1));
        read(f,e);
        if (e>=0) and (e<=3) then b[e]:=true;
      end;
      b[0]:=b[0] and b[1] and b[2] and b[3];
      if not b[0] then begin
        seek(f,98);
        c:=255;
        write(f,c);
        write(f,c);
        writeln('War of Succession has been reactivated.');
      end else writeln('Eliminate at least one rival to continue.');
    end;
  end else begin
    writeln('The War of Succession has been finished.');
    seek(f,96);
    read(f,c);
    if c>=50 then begin
      seek(f,18);
      read(f,c);
      if c mod 2=0 then begin
        writeln;
        writeln('Do you want to declare an independence?..');
        writeln;
        writeln('(Hall of Fame is not enabled. No negotiations nor new colonies are allowed.');
        writeln('You can''t fight European powers, yet they can attack you.');
        writeln('There''s no intervention units whatsoever.');
        writeln('However, Tory General may hesitate to attack your forces.');
        writeln('You better come prepared and sign peace treaties while there''s still time).');
        writeln;
        writeln('...Type ''y'' or ''yes'' if you do.');
        readln(confirm);
        if (confirm='yes') or (confirm='y') then begin
          inc(c);
          seek(f,18);
          write(f,c);
          unfreeze(true);
          writeln('That''s it, the War has begun.');
        end;
      end else if bit(c,3)=1 then begin
        writeln;
        writeln('You won the War. Do you want to continue in a normal mode?');
        writeln;
        writeln('...Type ''y'' or ''yes'' if you do.');
        readln(confirm);
        if (confirm='yes') or (confirm='y') then begin
          dec(c);
          seek(f,18);
          write(f,c);
          unfreeze(false);
          seek(f,50);
          c:=0;
          write(f,c);
          seek(f,98);
          c:=10;
          write(f,c);
          c:=0;
          write(f,c);
          writeln('That''s it, the War has been finished.');
        end;
      end;
    end;
  end;
  close(f);
end.